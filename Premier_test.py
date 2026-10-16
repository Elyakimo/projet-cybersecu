import re
from datetime import datetime

pattern = re.compile(r"Failed password", flags=re.MULTILINE)

datetime = datetime.strptime("Oct 10 22:46:01", "%b %d %H:%M:%S")
test_string = ("Oct 10 22:46:01 metasploitable sshd[4770]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.12 \n"
	"Oct 10 22:46:03 metasploitable sshd[4770]: Failed password for invalid user admin from 10.0.0.12 port 60856 ssh2\n"
	"Oct 10 22:46:04 metasploitable sshd[4770]: pam_unix(sshd:auth): check pass; user unknown\n"
	"Oct 10 22:46:06 metasploitable sshd[4770]: Failed password for invalid user admin from 10.0.0.12 port 60856 ssh2\n"
	"Oct 10 22:02:31 metasploitable sudo: pam_unix(sudo:session): session opened for user root by msfadmin(uid=0)\n"
	"Oct 10 22:02:31 metasploitable sudo: pam_unix(sudo:session): session closed for user root")

substitution = ""

result = pattern.sub(substitution, test_string)

print(datetime)
