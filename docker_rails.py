#!/usr/bin/env python3
import sys, os, glob
import subprocess
import argparse

NAME="docker_rails"

versions = {
        '7.0.1': 'wxwmatt/rails:7.0.1-alpine3.15'
        }

def get_rails_image_name(version):
    global versions
    return versions[version]

# Docker version 20.10.11, build dea9396
def generate_rails_project(name, options, rails_options):
    image_name = get_rails_image_name(options.rails)
    uid = os.getuid()
    gid = os.getgid()
    cwd = os.getcwd()
    args = ["docker", "run", "--rm", "-it","--user", f'{uid}:{gid}', "-v", f'{cwd}:/app:rw', "-e", "HOME=/app", "-w", "/app", image_name, "rails"] + rails_options
    subprocess.run(args)

def build_images(versions):
    for major in versions:
        for dockerfile in glob.glob(f'rails{major}/Dockerfile.rails*'):
            version = dockerfile.replace(f'rails{major}/Dockerfile.rails',"")
            image=f'wxwmatt/rails:{version}-alpine3.15'
            args = ["docker", "build", "-f", dockerfile, "-t", image, f'rails{major}/']
            print(f'Build {dockerfile}...');
            result = subprocess.run(args, stdout=subprocess.PIPE)
            if result.returncode != 0:
                print(result.stdout.replace("\\n","\n").decode("UTF-8"))
            else:
                print('Build successfully')

def build(args):
    print("Build images")
    versions = [args.version]
    import pdb;pdb.set_trace()
    build_images(versions)

def project(args):
    import pdb;pdb.set_trace()
    print("project")


parser = argparse.ArgumentParser(prog=NAME)
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

parser_build = subparsers.add_parser('build', help='Build rails images')
parser_build.add_argument('-v', '--version', type=str, help='Build a specific version')
parser_build.set_defaults(func=build)

parser_project = subparsers.add_parser('project', help='Create a new rails project')
parser_project.add_argument('--mysql', dest="database", action='store_const', const="mysql", help='Using MySQL')
parser_project.add_argument('--pq', dest="database", action='store_const', const="postgresql",  help='Using Postgresql')
parser_project.add_argument('--sqlite', dest="database", action='store_const', const="sqlite", help='Using SQLite3')
parser_project.set_defaults(func=project)


if len(sys.argv) == 1:
    parser.print_help()
    exit(1)
# parse some argument lists
opts = parser.parse_args(sys.argv[1:])
opts.func(opts);
