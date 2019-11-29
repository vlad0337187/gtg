#!/usr/bin/env python3

import os
import sys

from xml.dom.minidom import parse
from xdg.BaseDirectory import xdg_data_home


def anonymize(filename, outputfile):
    try:
        dom = parse(filename)
    except Exception as err:
        print("error while parsing %s: %s" % (filename, err))
        return

    tasks = dom.getElementsByTagName("task")

    for task in tasks:
        textnode = task.getElementsByTagName("title")[0].childNodes[0]
        nodevalue = textnode.nodeValue
        newnodevalue = ""

        for i in range(len(nodevalue)):
            if nodevalue[i] not in [" ", "\t", "\n"]:
                newnodevalue = newnodevalue + "m"
            else:
                newnodevalue = newnodevalue + nodevalue[i]

        textnode.nodeValue = newnodevalue

        contentnode = task.getElementsByTagName("content")
        if len(contentnode) == 0:
            continue

        contentnode = contentnode[0].childNodes[0]

        nodevalue = contentnode.nodeValue
        newnodevalue = ""

        for i in range(len(nodevalue)):
            if nodevalue[i] not in [" ", "\t", "\n"]:
                newnodevalue = newnodevalue + "m"
            else:
                newnodevalue = newnodevalue + nodevalue[i]

        contentnode.nodeValue = newnodevalue

    try:
        fp = open(outputfile, "w")
        fp.write(dom.toxml())
    except Exception as err:
        print("error while saving output file: %s" % err)


def usage():
    print("Usage: %s [taskfile] [outputfile]" % sys.argv[0])
    print()
    print("Removes private data from specified taskfile, or your")
    print("default gtg tasks file if unspecified.  Writes output")
    print("to /tmp/gtg-tasks.xml by default, or to specified")
    print("outputfile if provided.")
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        xmlfile = sys.argv[1]
    else:
        try:
            data_dir = os.path.join(xdg_data_home, "gtg")
            project_filepath = os.path.join(data_dir, "projects.xml")
            dom = parse(project_filepath)
            xmlproject = dom.getElementsByTagName("backend")[0]
            xmlfile = str(xmlproject.getAttribute("path"))
            xmlfile = os.path.join(data_dir, xmlfile)

            print("Reading tasks from %s" % (xmlfile))
        except:
            print()
            usage()

    if len(sys.argv) > 2:
        outputfile = sys.argv[2]
    else:
        # Use a reasonable default, and write out where it's sent
        outputfile = "/tmp/gtg-tasks.xml"
        print("Saving anonymized tasks to %s" % (outputfile))

    anonymize(xmlfile, outputfile)

if __name__ == "__main__":
    main()
