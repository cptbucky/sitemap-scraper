import sys
import os


class TreeConsoleWriter:
    def __init__(self):
        pass

    def write(self, sitemap):
        for entry in sitemap:
            if entry[0] is None:
                self.__write_sitemap_entry(sitemap, entry, 1)

    def __write_sitemap_entry(self, sitemap, entry, depth):
        depth_indicator = "|    " * depth
        sys.stdout.write(f"{depth_indicator} {entry[1]}{os.linesep}")

        if len(entry[2]) > 0:
            for child_entry_index in entry[2]:
                self.__write_sitemap_entry(sitemap, sitemap[child_entry_index], depth + 1)
