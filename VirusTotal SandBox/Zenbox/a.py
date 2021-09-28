#!/usr/bin/python
import os, sys, shutil

cdrom_dir = "e:\\"

work_dir = "c:\\mydownload\\"

script_name = "run_task.py"

script_in_cdrom = os.path.join(cdrom_dir, script_name)

script_in_work_dir = os.path.join(work_dir, script_name)

print("waiting ......")

while True:
	if os.path.isfile(script_in_cdrom):
		break

shutil.copytree(cdrom_dir, work_dir)

cmd = 'python %s' % script_in_work_dir

os.system(cmd)