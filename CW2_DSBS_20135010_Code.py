import sensors
import time
import graphs
import filters

HIGH_PASS_CONSTANT = .3
LOW_PASS_CONSTANT = 0.001
THRESHOLD = 445
SAMPLE_TIME = 0.005
sound1_pin=0
sound2_pin=1
sound3_pin=2
# tell the sensor module which sensors
# we have attached to which pins
sensor_pins={ "sound1":sound1_pin,"sound2":sound2_pin,"sound3":sound3_pin}
sensors.set_pins(sensor_pins)

#high-pass filter to detect only high frequency sounds
hpfilter1 = filters.HighPassFilter.make_from_time_constant(HIGH_PASS_CONSTANT,SAMPLE_TIME)
hpfilter2 = filters.HighPassFilter.make_from_time_constant(HIGH_PASS_CONSTANT,SAMPLE_TIME)
hpfilter3 = filters.HighPassFilter.make_from_time_constant(HIGH_PASS_CONSTANT,SAMPLE_TIME)

lpfilter1 = filters.LowPassFilter.make_from_time_constant(LOW_PASS_CONSTANT,SAMPLE_TIME)
lpfilter2 = filters.LowPassFilter.make_from_time_constant(LOW_PASS_CONSTANT,SAMPLE_TIME)
lpfilter3 = filters.LowPassFilter.make_from_time_constant(LOW_PASS_CONSTANT,SAMPLE_TIME)


frontistriggered = False
rightistriggered = False
leftistriggered = False

maxsound1 = 0
maxsound2 = 0
maxsound3 = 0
#these counters are just to assign the maxsound once in the start
count1=0
count2=0
count3=0

times=0


print("warning,frontsound,rightsound,leftsound,times")
while True:
	s1=sensors.sound1.get_level()
	s2=sensors.sound2.get_level()
	s3=sensors.sound3.get_level()
	#high-pass filtering each sound input
	sound_highpassed1 = hpfilter1.on_value(s1)
	sound_highpassed2 = hpfilter2.on_value(s2)
	sound_highpassed3 = hpfilter3.on_value(s3)
	#low-pass filtering each sound high-pass input
	sound_lowpassed1 = lpfilter1.on_value(sound_highpassed1)
	sound_lowpassed2 = lpfilter2.on_value(sound_highpassed2)
	sound_lowpassed3 = lpfilter3.on_value(sound_highpassed3)

	if sound_lowpassed1 > THRESHOLD and sound_lowpassed1 > sound_lowpassed2 and sound_lowpassed1>sound_lowpassed3:
		frontistriggered = True
	elif sound_lowpassed2 > THRESHOLD and sound_lowpassed2 > sound_lowpassed1 and sound_lowpassed2>sound_lowpassed3:
		rightistriggered = True
	elif sound_lowpassed3 > THRESHOLD and sound_lowpassed3 > sound_lowpassed2 and sound_lowpassed3>sound_lowpassed1:
		leftistriggered = True


	if frontistriggered:
		count2=0
		count3=0
		if count1 == 0 :
			times+=1
			maxsound1 = sound_lowpassed1
			count1+=1
			print("LEAVE-LOUD SOUND AS MUCH AS",sound_lowpassed1,0,0,times,sep=',')
		else:
			times+=1
			if sound_lowpassed1 > maxsound1:
				print("SOUND IS GETTING WORSE WITH",sound_lowpassed1,0,0,times,sep=',')
				maxsound1 = sound_lowpassed1
			else:
				print("LEAVE-LOUD SOUND AS MUCH AS",sound_lowpassed1,0,0,times,sep=',')


	elif rightistriggered:
		count1=0
		count3=0
		if count2 == 0 :
			times+=1
			maxsound2 = sound_lowpassed2
			count2+=1
			print("LEAVE TO THE LEFT LOUD SOUND AS",0,sound_lowpassed2,0,times,sep=',')
		else:
			times+=1
			if sound_lowpassed2 > maxsound2:
				print("SOUND IS GETTING WORSE LEAVE TO THE LEFT WITH",0,sound_lowpassed2,0,times,sep=',')
				maxsound2 = sound_lowpassed2
			else:
				print("LEAVE TO THE LEFT LOUD SOUND AS",0,sound_lowpassed2,0,times,sep=',')

	elif leftistriggered:
		count1=0
		count2=0
		if count3 == 0 :
			times+=1

			maxsound3 = sound_lowpassed3
			count3+=1
			print("LEAVE TO THE RIGHT LOUD SOUND AS MUCH AS",0,0,sound_lowpassed3,times,sep=',')
		else:
			times+=1

			if sound_lowpassed3 > maxsound3:
				print("SOUND IS GETTING WORSE LEAVE TO THE RIGHT WITH",0,0,sound_lowpassed3,times,sep=',')
				maxsound3 = sound_lowpassed3
			else:
				print("LEAVE TO THE RIGHT LOUD SOUND AS MUCH AS",0,0,sound_lowpassed3,times,sep=',')



	frontistriggered = False
	rightistriggered = False
	leftistriggered = False
	time.sleep(0.1)
