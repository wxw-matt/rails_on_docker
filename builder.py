#!/usr/bin/env python3
import sys, os, glob
import subprocess
import argparse

NAME="builder"

def get_supported_versions():
    return [e.replace('rails', '') for e in glob.glob(f'rails[2-7]')]

def run_docker_cmd(cmd, output_error=True, output_stdout=True):
    print(cmd)
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
        rails_dir = f'rails{major}'
        files = glob.glob(f'{rails_dir}/Dockerfile.rails*')
        if files:
            exclude_files = {}
            if os.path.isfile(f'{rails_dir}/.rod_ignore'):
                with open (f'{rails_dir}/.rod_ignore') as f:
                    for line in f.readlines():
                        exclude_files[line.strip()] = True
                indices_to_remove = []
                for idx, f in enumerate(files):
                    if f.replace(f'{rails_dir}/', '') in exclude_files:
                        indices_to_remove.append(idx)

                for idx in indices_to_remove:
                    del files[idx]

            image_info = []
            for f in files:
                image_tag = None
                with open(f) as fo:
                    for line in fo.readlines():
                        if '# Tag:' in line:
                            image_tag = line.replace('# Tag:','').strip()
                            break

                if image_tag is None:
                    raise Exception(f"Not image tag in Dockerfile {f}")
                version = f.replace(f'rails{major}/Dockerfile.rails',"")
                cmd = ["docker", "build", "--load", "-f", f, "-t", image_tag, f'rails{major}/']
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
                print(f'Building {image_info["dockerfile"]} with tag: {image_info["image_tag"]}...')
                if build_image(image_info).returncode == 0:
                    print('Build successfully')
                    if push:
                        print(f'Pushing {image_tag}')
                        if push_image(image_tag, output_stdout=True).returncode == 0:
                            print(f'Pushed {image_tag} successfully')
                        else:
                            print(f"Failed to push {image_tag}")
                else:
                    print(f"Failed to build {image_tag}: {image_info}")
    else:
        print("Couldn't find Dockerfiles for version: " + str(versions))

def build(args):
    print("Building images")
    versions = [args.version] if args.version else None
    build_images(versions, push=args.push)

parser = argparse.ArgumentParser(prog=NAME)
subparsers = parser.add_subparsers(help='sub-command help')

parser_build = subparsers.add_parser('build', help='Build rails images')
parser_build.add_argument('-v', '--version', type=str, help='Build a specific version')
parser_build.add_argument('-p', '--push', action='store_true', help='Push the images to Docker hub after building')
parser_build.set_defaults(func=build)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)
# parse some argument lists
opts = parser.parse_args(sys.argv[1:])
opts.func(opts)
