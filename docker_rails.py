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

def get_supported_versions():
    return [e.replace('rails') for e in glob.glob(f'rails[2-7]')]


def run_docker_cmd(cmd, output_error=True, output_stdout=False):
    if output_stdout:
        result = subprocess.run(cmd)
    else:
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
    if result.returncode != 0 and output_error:
        print(result.stdout.decode("UTF-8"))
    return result

def collect_dockerfiles(versions):
    dockerfiles = {}
    for major in versions:
        files = glob.glob(f'rails{major}/Dockerfile.rails*')
        if files:
            image_info = []
            for f in files:
                version = f.replace(f'rails{major}/Dockerfile.rails',"")
                image_tag = f'wxwmatt/rails:{version}-alpine3.15'
                cmd = ["docker", "build", "-f", f, "-t", image_tag, f'rails{major}/']
                image_info.append({
                    'version': version,
                    'image_tag': image_tag,
                    'docker_cmd': cmd,
                    'dockerfile': f
                })
            dockerfiles[major]=image_info
    return dockerfiles


def push_images(image_tags):
    for image_tag in image_tags:
        cmd = ["docker", "push", image_tag]
        run_docker_cmd(cmd)

def push_image(image_tag, output_stdout=False):
    cmd = ["docker", "push", image_tag]
    return run_docker_cmd(cmd, output_stdout=output_stdout)


def build_image(image_info):
    version = image_info['version']
    image_tag = image_info['image_tag']
    docker_cmd = image_info['docker_cmd']
    dockerfile = image_info['dockerfile']
    return run_docker_cmd(docker_cmd)

def build_images(versions, push=False):
    versions = versions or get_supported_versions()
    dockerfiles = collect_dockerfiles(versions)
    if dockerfiles:
        print(f'{len(dockerfiles)} Dockerfiles found')
        for major,v in dockerfiles.items():
            for image_info in v:
                image_tag = image_info['image_tag']
                print(f'Building {image_info["dockerfile"]}...')
                if build_image(image_info).returncode == 0:
                    print('Build successfully')
                    if push:
                        print(f'Pushing {image_tag}')
                        if push_image(image_tag, output_stdout=True).returncode == 0:
                            print(f'Pushed {image_tag} successfully')
                        else:
                            print(f"Failed to push {image_tag}")
                else:
                    print("Couldn't find Dockerfiles for major version: " + major)

def build(args):
    print("Build images")
    versions = [args.version]
    build_images(versions, push=args.push)

def project(args):
    print("project")


parser = argparse.ArgumentParser(prog=NAME)
parser.add_argument('--foo', action='store_true', help='foo help')
subparsers = parser.add_subparsers(help='sub-command help')

parser_build = subparsers.add_parser('build', help='Build rails images')
parser_build.add_argument('-v', '--version', type=str, help='Build a specific version')
parser_build.add_argument('-p', '--push', action='store_true', help='Push the images to Docker hub after building')
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
