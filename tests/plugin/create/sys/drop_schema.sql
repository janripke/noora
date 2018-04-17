print "drop schema $(username)"
drop schema if exists $(username)

print "drop user $(username)"
drop user $(username)
drop login $(username)