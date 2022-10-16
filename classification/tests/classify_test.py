text_input_bad_one = """Billions of people on every continent are suffering because of climate change, according to a major new United Nations report released on Monday. And governments must do a better job of protecting the most vulnerable communities while also rapidly reducing greenhouse gas emissions.
    The report by nearly 300 top scientists from around the world paints a picture of a planet already transformed by greenhouse gas emissions and teetering on the brink of widespread, irreversible damage.
    "People are now suffering and dying from climate change," says Kristie Ebi, one of the lead authors of the report and an epidemiologist at the University of Washington. """

print("BAD")
print(calculate_score(text_input_bad_one))

text_input_good_one = """Truck driver Gary Wilburn was named a Highway Angel for offering aid to an injured Arkansas state trooper who was pinned inside his vehicle after a serious crash.

The Truckload Carriers Association bestowed the honor and shared the ‘incredible story.’

On the afternoon of October 4, near Forrest City, Arkansas, Wilburn was driving very slowly in heavy traffic. He came across a crashed State Trooper’s vehicle on the side of the road. Every other motorist was passing the vehicle without stopping to look inside.

“I was in traffic for an hour before I saw the trooper,” said the trucker from San Antonio, Texas. “Some of the stuff I noticed was insane—no one’s calling the police, cars are driving by, and no one stopped to help him.”

Wilburn, who drives for Anderson Trucking, called 911 and reported what he found.

LOOK: 13 Truckers Use Their Vehicles to Prevent Suicide Attempt From Ending a Life

“He was banged up really bad,” Wilburn said. “Lower legs were broken, upper legs were broken and he was pinned in. His legs were crushed really bad.”

He then stayed with the trapped officer until emergency personnel arrived and he was airlifted to a local hospital.

Wilburn, who is still upset that no one had stopped, did not know what caused the accident, but says he is usually the man for the job.

“I’m that idiot that runs into burning buildings and pulls out pets. When I see something like that, I can’t keep going on about my day.”

Since the program’s inception in August 1997, nearly 1,300 professional truck drivers have been recognized as Highway Angels for exemplary kindness, courtesy, and courage displayed while on the job."""
print("GOOD")
print(calculate_score(text_input_good_one))

print("BAD")
text_input_good_two = "That's bad"
print(calculate_score(text_input_good_two))


print("GOOD")
t_i_g_3 = "That's great!"
print(calculate_score(t_i_g_3))