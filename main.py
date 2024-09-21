if __name__ == "__main__":
    print("Starting the application")

    import os
    import time
    from app import DriveClient, GradeReader, GradesClient
    from app.utils import get_env

    env = get_env()

    force_renew = input(
        "Forcefully regenerate credentials? (Press enter to skip) ") != ""

    gr = GradeReader()
    dc = DriveClient(force_renew=force_renew)
    gc = GradesClient(
        env.get("SALESFORCE_USERNAME"),
        env.get("SALESFORCE_PASSWORD"),
        env.get("SALESFORCE_SECURITY_TOKEN"),
        env.get("SALESFORCE_DOMAIN"),
    )

    print("Getting files from Google Drive")
    time.sleep(0.5)
    link = input("Enter the link to the drive folder: ")

    folder_id = link.split("/")[-1]
    dc.download_files(folder_id)

    print()
    print("Reading grades from the downloaded files")

    grades = []
    for file in os.listdir(".temp"):
        gs = gr.read_grades_from_xlsx(f".temp/{file}")
        grades.extend(gs)

    print()
    print(f"Collected {len(grades)} grades")
    time.sleep(0.5)
    print()

    if input("Uploading grades to Salesforce (enter to continue; anything else to skip) ") == "":
        for grade in grades:
            gc.upload(grade)
            print(f"Uploaded {grade}")

    print()

    # remove the temp folder
    for file in os.listdir(".temp"):
        os.remove(f".temp/{file}")
    os.rmdir(".temp")

    print("Task completed")
