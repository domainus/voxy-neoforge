#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def find_jar_file(project_dir: Path) -> Path | None:
    libs_dir = project_dir / "build" / "libs"
    if not libs_dir.is_dir():
        return None

    jars = [jar for jar in libs_dir.glob("*.jar") if "sources" not in jar.name]
    if not jars:
        return None

    return max(jars, key=lambda jar: (jar.stat().st_mtime_ns, jar.name))


def validate_mixin_config(json_file: Path, jar_entries: set[str]) -> tuple[int, int, int]:
    config_errors = 0
    missing_classes = 0
    total_mixins = 0

    print(f"Checking {json_file.name}...")

    try:
        with json_file.open("r", encoding="utf-8") as handle:
            config = json.load(handle)
    except json.JSONDecodeError as exc:
        print(f"{RED}  ✗ Invalid JSON syntax{NC}")
        print(f"{YELLOW}    {exc.msg} at line {exc.lineno}, column {exc.colno}{NC}")
        return 1, 0, 0

    package = config.get("package")
    if not isinstance(package, str) or not package:
        print(f"{RED}  ✗ Missing package declaration{NC}")
        return 1, 0, 0

    for array_type in ("mixins", "client", "server"):
        mixins = config.get(array_type, [])
        if not mixins:
            continue
        if not isinstance(mixins, list):
            print(f"{RED}  ✗ .{array_type} must be an array{NC}")
            config_errors += 1
            continue

        print(f"  Validating .{array_type}[]...")
        for mixin in mixins:
            if not isinstance(mixin, str) or not mixin:
                print(f"{RED}    ✗ Invalid mixin entry in .{array_type}[]{NC}")
                config_errors += 1
                continue

            total_mixins += 1
            class_path = f"{package.replace('.', '/')}/{mixin.replace('.', '/')}.class"
            if class_path in jar_entries:
                print(f"    {GREEN}✓{NC} {mixin}")
                continue

            print(f"    {RED}✗ {mixin}{NC}")
            print(f"      {YELLOW}Expected: {class_path}{NC}")
            print(f"      {YELLOW}Status: NOT FOUND IN JAR{NC}")
            missing_classes += 1

    print("")
    return config_errors, missing_classes, total_mixins


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that mixins declared in JSON configs exist in the built JAR."
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Project root containing src/main/resources and build/libs (defaults to current directory).",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()

    print("=== MIXIN CONFIGURATION VALIDATION ===")
    print("")

    jar_file = find_jar_file(project_dir)
    if jar_file is None:
        print(f"{RED}ERROR: No JAR file found in build/libs/{NC}")
        print("Run './gradlew build' first")
        return 1

    print(f"Validating JAR: {jar_file.name}")
    print("")

    with zipfile.ZipFile(jar_file) as jar_handle:
        jar_entries = set(jar_handle.namelist())

    resource_dir = project_dir / "src" / "main" / "resources"
    mixin_configs = sorted(resource_dir.glob("*.mixins.json"))
    if not mixin_configs:
        print(f"{YELLOW}WARNING: No mixin configuration files found{NC}")
        return 0

    config_errors = 0
    missing_classes = 0
    total_mixins = 0

    for config_file in mixin_configs:
        file_config_errors, file_missing_classes, file_total_mixins = validate_mixin_config(
            config_file, jar_entries
        )
        config_errors += file_config_errors
        missing_classes += file_missing_classes
        total_mixins += file_total_mixins

    print("=== VALIDATION SUMMARY ===")
    print(f"Total mixins checked: {total_mixins}")
    print(f"JAR file: {jar_file.name}")
    print(f"JAR size: {jar_file.stat().st_size // 1024 // 1024}M")
    print("")

    if config_errors == 0 and missing_classes == 0:
        print(f"{GREEN}✓ ALL CHECKS PASSED{NC}")
        print("All mixin references are valid and present in JAR")
        return 0

    total_issues = config_errors + missing_classes
    print(f"{RED}✗ VALIDATION FAILED{NC}")
    print(f"Found {total_issues} validation issue(s)")
    if config_errors:
        print(f"Configuration errors: {config_errors}")
    if missing_classes:
        print(f"Missing classes: {missing_classes}")
    print("")

    if config_errors:
        print("Configuration issues detected in mixin JSON files.")
        print("These must be fixed before mixins can load correctly.")
        print("")

    if missing_classes:
        print("These mixins are declared in JSON configs but missing from the JAR.")
        print("This will cause ClassNotFoundException at runtime.")
        print("")
        print("Common causes:")
        print("  1. Mixin class excluded from compilation (check build.gradle sourceSets)")
        print("  2. Mixin class deleted but not removed from JSON")
        print("  3. Typo in mixin class name")

    return 1


if __name__ == "__main__":
    sys.exit(main())
