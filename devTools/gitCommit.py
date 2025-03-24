import os
import shutil
import subprocess

# === Constants ===
project_name = "cuntytabletops"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.dirname(project_root)

dev_copy = os.path.join(parent_dir, f"{project_name}-dev")
pub_copy = os.path.join(parent_dir, f"{project_name}-pub")

# === UI ===
print("\n🧠 Welcome to CuntyCommit™®©")
print("--------------------------------------")
print("What would you like to copy?")
print("1. 🔒 cuntyTabletops-dev (private)")
print("2. 🌍 cuntyTabletops-pub (public)")
print("3. 😎 both baby!")

target = input("Select an option (1/2/3): ")
commit_msg = input("📝 Enter your commit message: ")
print("")

# === Functions ===

def copy_project(destination):
    shutil.copytree(project_root, destination)
    print(f"📦 Project copied to: {destination}")

def copy_dev_config_into_pub(pub_path):
    source = os.path.join(pub_path, "devTools", "config.json")
    destination = os.path.join(pub_path, "resources", "config.json")
    shutil.copy(source, destination)
    print("🔁 Replaced public config with devTools/config.json")

def remove_devtools_folder_from_pub(pub_path):
    devtools_folder = os.path.join(pub_path, "devTools")
    if os.path.exists(devtools_folder):
        shutil.rmtree(devtools_folder)
        print("🧹 Removed /devTools folder from public copy")

def commit_and_push(repo_path, remote_name, commit_msg):
    print(f"📍 Committing to {remote_name} in {repo_path}")
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], check=True)

    force = input(f"🤔 Force push to {remote_name}? (y/N): ").strip().lower() == "y"
    push_cmd = ["git", "push"]
    if force:
        push_cmd.append("--force")
    push_cmd += [remote_name, "main"]

    subprocess.run(push_cmd, check=True)
    print(f"🚀 Pushed to {remote_name}!\n")

# === Actions ===

try:
    if target == "1":
        print("🔒 Creating dev copy...")
        copy_project(dev_copy)
        commit_and_push(dev_copy, "origin", commit_msg)

    elif target == "2":
        print("🌍 Creating public copy...")
        copy_project(pub_copy)
        copy_dev_config_into_pub(pub_copy)
        remove_devtools_folder_from_pub(pub_copy)
        commit_and_push(pub_copy, "origin", commit_msg)

    elif target == "3":
        print("😎 Creating both dev and public copies...")
        copy_project(dev_copy)
        copy_project(pub_copy)
        copy_dev_config_into_pub(pub_copy)
        remove_devtools_folder_from_pub(pub_copy)
        commit_and_push(dev_copy, "origin", commit_msg)
        commit_and_push(pub_copy, "origin", commit_msg)

    else:
        print("❌ Invalid option. Nothing was copied or committed.")

except subprocess.CalledProcessError as e:
    print(f"❌ Git command failed: {e}")

print("\n✅ Done.")
