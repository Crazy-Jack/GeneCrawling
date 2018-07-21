import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('jacklitianqin@gmail.com', 'qaz1wsx2@gmail')

msg = "Hi, this is the first auto-email test"

server.sendmail("jacklitianqin@gmail.com", "jacklitianqin@berkeley.edu", msg)

server.quit()