import os
import sys
import json
import argparse
sys.path.append("../Utility")
from file import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruction system")
    parser.add_argument("config", help="path to the config file")
    parser.add_argument("--make",
            help="Step 1) make fragments from RGBD sequence",
            action="store_true")
    parser.add_argument("--register",
            help="Step 2) register all fragments to detect loop closure",
            action="store_true")
    parser.add_argument("--refine",
            help="Step 3) refine rough registrations", action="store_true")
    parser.add_argument("--integrate",
            help="Step 4) integrate the whole RGBD sequence to make final mesh",
            action="store_true")
    parser.add_argument("--debug_mode", help="turn on debug mode",
            action="store_true")
    args = parser.parse_args()

    if not args.make and \
            not args.register and \
            not args.refine and \
            not args.integrate:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # check folder structure
    if args.config is not None:
        with open(args.config) as json_file:
            config = json.load(json_file)
            check_folder_structure(config["path_dataset"])
    assert config is not None

    if args.debug_mode:
        config['debug_mode'] = True
    else:
        config['debug_mode'] = False

    if args.make:
        import make_fragments
        make_fragments.run(config)
    if args.register:
        import register_fragments
        register_fragments.run(config)
    if args.refine:
        import refine_registration
        refine_registration.run(config)
    if args.integrate:
        import integrate_scene
        integrate_scene.run(config)
