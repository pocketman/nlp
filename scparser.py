import xml.etree.ElementTree as ET
import os
from os.path import isfile

BR1 = 'semcor3.0/brown1/tagfiles/'
BR2 = 'semcor3.0/brown2/tagfiles/'

def getTree(folder):
    filenames = []
    for f in os.listdir(folder):
        filenames.append(f)
    root = ET.Element('root')
    for f in filenames:
        tree = ET.parse(folder+f)
        subelm = tree.getroot().find('context')
        root.append(subelm)
    return root
