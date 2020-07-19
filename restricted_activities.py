def check_restricted_activities(message):

	closed_activities = ['night club', 'music festival']

	restricted_activities = {
		
		"pub":
			'''
			Maximum of 10 people per booking or table.
			Alcohol can only be consumed by seated customers.
			''',

		"visit family and friends at home":
			''' 
			No more than 20 visitors in one household in total.
			''',
			
		"park":
			'''
			No more than 20 people are allowed to gather outside in a public place.
			''',
		
		"gym":
			'''
			A maximum of 20 people per class applies to gym and recreational classes.
			'''
		
	}
	message = message.lower()
	if message in restricted_activities:
		condition = restricted_activities.get(message)
		response = f"Yes, some relevant restrictions for {message}s are:{condition}"
	elif message in closed_activities:
		response = f"Sorry {message}s are CLOSED! You can't go."
	else:
		# restaurant, cafe, recreational class, funeral, wedding, school, uni
		response = "Keep a 1.5m distance from others.\nThe number of people in a public place must not exceed one person per 4 square metres."
	return response

message = input('message')
print(check_restricted_activities(message))