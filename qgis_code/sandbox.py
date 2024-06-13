import subprocess

p1 = subprocess.Popen('dir', shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p2 = subprocess.Popen('sort /R', shell=True, stdin=p1.stdout)

p1.stdout.close()
out, err = p2.communicate()