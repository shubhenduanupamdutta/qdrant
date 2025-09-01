#!/usr/bin/env python3
"""
Qdrant Development Helper Script

This script helps new contributors get started with Qdrant development.
It provides utilities for building, testing, and exploring the codebase.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def run_command(cmd, description="", check=True):
    """Run a shell command with proper error handling."""
    print(f"🔄 {description or cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False

def check_prerequisites():
    """Check if required tools are installed."""
    print("🔍 Checking prerequisites...")
    
    tools = {
        "rustc --version": "Rust compiler",
        "cargo --version": "Cargo package manager",
        "git --version": "Git version control"
    }
    
    all_good = True
    for cmd, name in tools.items():
        if not run_command(cmd, f"Checking {name}", check=False):
            print(f"❌ {name} not found. Please install it first.")
            all_good = False
        else:
            print(f"✅ {name} is available")
    
    return all_good

def setup_dev_environment():
    """Set up the development environment."""
    print("🛠️  Setting up development environment...")
    
    commands = [
        ("rustup component add rustfmt clippy", "Installing rustfmt and clippy"),
        ("rustup install nightly", "Installing nightly Rust toolchain"),
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc, check=False):
            print(f"⚠️  Warning: {desc} failed, but continuing...")

def build_project(release=False):
    """Build the Qdrant project."""
    build_type = "release" if release else "debug"
    cmd = "cargo build" + (" --release" if release else "")
    
    print(f"🔨 Building Qdrant ({build_type})...")
    return run_command(cmd, f"Building in {build_type} mode")

def run_tests(specific_test=None):
    """Run tests for the project."""
    if specific_test:
        cmd = f"cargo test {specific_test}"
        desc = f"Running tests for {specific_test}"
    else:
        cmd = "cargo test"
        desc = "Running all tests"
    
    print("🧪 Running tests...")
    return run_command(cmd, desc, check=False)

def check_code_quality():
    """Run code formatting and linting checks."""
    print("🔍 Checking code quality...")
    
    commands = [
        ("cargo +nightly fmt --all -- --check", "Checking code formatting"),
        ("cargo clippy --workspace --all-features", "Running clippy lints"),
    ]
    
    all_passed = True
    for cmd, desc in commands:
        if not run_command(cmd, desc, check=False):
            all_passed = False
    
    return all_passed

def explore_codebase():
    """Provide guidance for exploring the codebase."""
    print("🗺️  Codebase exploration suggestions:")
    
    exploration_tips = [
        ("src/main.rs", "Start here - main application entry point"),
        ("lib/api/", "API definitions and gRPC interfaces"),
        ("lib/collection/", "Collection management and operations"),
        ("lib/segment/", "Core vector storage and indexing"),
        ("lib/storage/", "Persistence and storage management"),
        ("tests/", "Integration tests and examples"),
        ("config/", "Configuration files and examples"),
    ]
    
    print("\n📁 Key directories to explore:")
    for path, description in exploration_tips:
        if os.path.exists(path):
            print(f"  ✅ {path:<20} - {description}")
        else:
            print(f"  ❌ {path:<20} - {description} (not found)")
    
    print("\n🔍 Useful commands for exploration:")
    commands = [
        ("find . -name '*.rs' | head -20", "List first 20 Rust files"),
        ("grep -r 'TODO\\|FIXME' --include='*.rs' src/ lib/", "Find TODOs (contribution opportunities)"),
        ("cargo doc --open", "Generate and open documentation"),
        ("git log --oneline -10", "Recent commits"),
    ]
    
    for cmd, desc in commands:
        print(f"  {cmd:<50} # {desc}")

def find_contribution_opportunities():
    """Find potential areas for contribution."""
    print("🎯 Finding contribution opportunities...")
    
    # Look for TODO comments
    print("\n📝 TODO comments (potential contribution areas):")
    run_command("grep -r 'TODO\\|FIXME' --include='*.rs' src/ lib/ | head -10", 
                "Searching for TODO comments", check=False)
    
    print("\n🐛 For more contribution opportunities:")
    print("  • Check GitHub issues: https://github.com/qdrant/qdrant/issues")
    print("  • Look for 'good first issue' label")
    print("  • Join Discord: https://discord.gg/tdtYvXjC4h")

def main():
    parser = argparse.ArgumentParser(description="Qdrant Development Helper")
    parser.add_argument("--setup", action="store_true", help="Set up development environment")
    parser.add_argument("--build", action="store_true", help="Build the project")
    parser.add_argument("--release", action="store_true", help="Build in release mode")
    parser.add_argument("--test", nargs="?", const="", help="Run tests (optionally specify which)")
    parser.add_argument("--check", action="store_true", help="Check code quality")
    parser.add_argument("--explore", action="store_true", help="Get codebase exploration guidance")
    parser.add_argument("--contrib", action="store_true", help="Find contribution opportunities")
    parser.add_argument("--all", action="store_true", help="Run all checks and builds")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        print("🚀 Qdrant Development Helper")
        print("Use --help to see available options")
        print("\nQuick start:")
        print("  python dev_helper.py --setup    # Set up environment")
        print("  python dev_helper.py --all      # Run full check")
        print("  python dev_helper.py --explore  # Get exploration guidance")
        return
    
    # Change to project root if script is run from elsewhere
    script_dir = Path(__file__).parent
    if script_dir.name != "qdrant":
        print("⚠️  Please run this script from the Qdrant project root directory")
        return
    
    success = True
    
    # Check prerequisites first
    if not check_prerequisites():
        print("❌ Prerequisites not met. Please install required tools.")
        return
    
    if args.setup or args.all:
        setup_dev_environment()
    
    if args.build or args.all:
        success &= build_project(release=args.release)
    
    if args.test is not None or args.all:
        success &= run_tests(args.test if args.test else None)
    
    if args.check or args.all:
        success &= check_code_quality()
    
    if args.explore:
        explore_codebase()
    
    if args.contrib:
        find_contribution_opportunities()
    
    if args.all:
        print(f"\n{'✅' if success else '❌'} Overall status: {'All checks passed!' if success else 'Some checks failed'}")

if __name__ == "__main__":
    main()
