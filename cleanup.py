import os
import shutil

# Path to the base folder containing all generated cases
output_base = "simulation_cases"

def delete_generated_cases(base_folder, exclude=None):
    """
    Deletes all generated case folders in the base folder.
    
    Args:
        base_folder (str): Path to the folder containing all generated cases.
        exclude (list): List of folder names or patterns to exclude from deletion.
    """
    exclude = exclude or []  # Default to an empty list if None
    if not os.path.exists(base_folder):
        print(f"Base folder '{base_folder}' does not exist.")
        return

    # List all subdirectories in the base folder
    case_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    print("The following folders will be deleted:")
    for folder in case_folders:
        if folder in exclude:
            print(f"Skipping {folder} (excluded).")
            continue
        print(f"- {folder}")

    # Confirm deletion
    confirmation = input("Do you want to proceed with deletion? (yes/no): ").strip().lower()
    if confirmation != "yes" and confirmation != "y":
        print("Deletion aborted.")
        return

    # Delete the folders
    for folder in case_folders:
        if folder in exclude:
            continue
        folder_path = os.path.join(base_folder, folder)
        shutil.rmtree(folder_path)
        print(f"Deleted {folder_path}")

    print("All selected folders have been deleted.")

# Example Usage
delete_generated_cases(output_base, exclude=["keep_this_case", "another_case_to_keep"])
