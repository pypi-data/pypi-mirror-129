b gunit::suite::run:end
b gunit::end

commands 1
 silent
 up
 p suite
 p test_name
 p test_reason
 p test_failed
 p test_elipsed
 p test_location
 c
end

commands 2
 silent
 set logging off
 quit
end

c
run
