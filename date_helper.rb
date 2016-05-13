# Proudly (or shamefully, depending on how you look at it) ripped right out
# of ActionView and modified to base it all on the Epoch. Give credit where credit is due.

# from_time expects another judgement from Epoch (e.g, Time.whatever.to_i)
def time_in_words(from_time, to_time = Time.now.to_i, include_seconds = false)
	distance_in_seconds = (to_time - from_time)
	if distance_in_seconds > 0
		time_in_words_late(from_time, to_time, include_seconds = false)
	else
		time_in_words_ontime(from_time, to_time, include_seconds = false)
	end
end

def time_in_words_late(from_time, to_time = Time.now.to_i, include_seconds = false)
	distance_in_minutes = (((to_time - from_time).abs)/60).round
	distance_in_seconds = ((to_time - from_time).abs).round

	case distance_in_minutes
	when 0..1
		return (distance_in_minutes==0) ? 'less than a minute ago' : '1 minute ago' unless include_seconds
		case distance_in_seconds
		when 0..5   then 'less than 5 seconds ago'
		when 6..10  then 'less than 10 seconds ago'
		when 11..20 then 'less than 20 seconds ago'
		when 21..40 then 'half a minute ago'
		when 41..59 then 'less than a minute ago'
		else             '1 minute ago'
		end

	when 2..45           then "#{distance_in_minutes} minutes ago"
	when 46..90          then 'about 1 hour ago'
	when 90..1440        then "about #{(distance_in_minutes / 60).round} hours ago"
	when 1441..2880      then '1 day ago'
	when 2881..43220     then "#{(distance_in_minutes / 1440).round} days ago"
	when 43201..86400    then 'about 1 month ago'
	when 86401..525960   then "#{(distance_in_minutes / 43200).round} months ago"
	when 525961..1051920 then 'about 1 year ago'
	else                      "over #{(distance_in_minutes / 525600).round} years ago"
	end
end

def time_in_words_ontime(from_time, to_time = Time.now.to_i, include_seconds = false)
	distance_in_minutes = (((to_time - from_time).abs)/60).round
	distance_in_seconds = ((to_time - from_time).abs).round

	case distance_in_minutes
	when 0..1
		return (distance_in_minutes==0) ? 'in less than a minute' : 'in 1 minute' unless include_seconds
		case distance_in_seconds
		when 0..5   then 'in less than 5 seconds'
		when 6..10  then 'in less than 10 seconds'
		when 11..20 then 'in less than 20 seconds'
		when 21..40 then 'in half a minute'
		when 41..59 then 'in less than a minute'
		else             'in 1 minute'
		end

	when 2..45           then "in #{distance_in_minutes} minutes"
	when 46..90          then 'in about 1 hour'
	when 90..1440        then "in about #{(distance_in_minutes / 60).round} hours"
	when 1441..2880      then 'in 1 day'
	when 2881..43220     then "in #{(distance_in_minutes / 1440).round} days"
	when 43201..86400    then 'in about 1 month'
	when 86401..525960   then "in #{(distance_in_minutes / 43200).round} months"
	when 525961..1051920 then 'in about 1 year'
	else                      "in over #{(distance_in_minutes / 525600).round} years"
	end
end
