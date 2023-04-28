"""Helper to sort through my Fuji camera's RAW and JPEG files."""

import os
import sys
import shutil

import pygame

SCREEN_SIZE = (1280, 720)

ACTION_KEEP_BOTH = pygame.K_k
ACTION_KEEP_JPEG = pygame.K_j
ACTION_KEEP_NONE = pygame.K_d

RESULT_KEEP_JPEG = "keep_jpeg"
RESULT_KEEP_BOTH = "keep_both"
RESULT_KEEP_NONE = "keep_none"
RESULT_QUIT = "quit"

screen = None

def process_jpeg(jpeg_path: str) -> str:
    """Reuturn RESULT_KEEP if entry should be kept, RESULT_DELETE otherwise."""

    img = pygame.image.load(jpeg_path)
    img = pygame.transform.scale(img, SCREEN_SIZE)
    screen.blit(img, (0, 0))

    while True:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return RESULT_QUIT
            
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == ACTION_KEEP_JPEG:
                return RESULT_KEEP_JPEG
            if event.key == ACTION_KEEP_BOTH:
                return RESULT_KEEP_BOTH
            if event.key == ACTION_KEEP_NONE:
                return RESULT_KEEP_NONE

        pygame.display.update()

def delete_file(deleted_dir: str, full_path: str):
    if not os.path.exists(full_path):
        print(f"Cannot delete {full_path}. It does not exist.")
        return

    print("Deleting", full_path)
    filename = os.path.normpath(os.path.basename(full_path))
    deleted_path = os.path.join(deleted_dir, filename)
    os.rename(full_path, deleted_path)

def main(directory: str):
    directory = os.path.abspath(directory)
    deleted = os.path.join(directory, ".delete")

    try:
        os.makedirs(deleted)
    except OSError:
        print("Directory .delete exists probably due to a crash. This could lead to data loss. Delete it and run again")
        return

    pygame.init()
    global screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    files = os.listdir(directory)
    files.sort()

    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext != ".JPG":
            continue

        path_noext = os.path.join(directory, name)
        path_jpeg = f"{path_noext}.JPG"
        path_raw = f"{path_noext}.RAF"

        result = process_jpeg(path_jpeg)
        if result == RESULT_QUIT:
            print("Quitting...")
            break
        elif result == RESULT_KEEP_JPEG:
            delete_file(deleted, path_raw)
        elif result == RESULT_KEEP_NONE:
            delete_file(deleted, path_raw)
            delete_file(deleted, path_jpeg)
        else:
            print("Keeping", path_jpeg, "and", path_raw)

    pygame.display.quit()

    deleted_files = os.listdir(deleted)
    print(f"Deleted files ({len(deleted_files)}): ", "\n  ".join(deleted_files))
    
    while True:
        response = input("What do do? [DELETE/QUIT] ")
        if response == "DELETE":
            shutil.rmtree(deleted)
            break
        elif response == "QUIT":
            break

    print("Done!")

if __name__ == "__main__":
    main(sys.argv[1])