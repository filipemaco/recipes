# ------ DB commands ----- #
# Creates an infrastructure (migrations files)
flask db init

# Migrate command
flask db migrate -m "users table"

# Upgrade db
flask db upgrade

# Downgrade
flask db downgrade


# Add data to table
"""
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()
"""

# color pallete
https://colorhunt.co/palette/167033

# correct the page according pycodestyle(https://github.com/hhatto/autopep8)
$ autopep8 --in-place --aggressive --aggressive <filename>


//USERS

user: filipemaco
pw: ??


user: test1user
pw: pass123

user: test3user
pw: pass123
