stadt = "Frankfurt"
temperatur = 18.5
ist_warm = temperatur > 20 

temperaturen = [12.1, 15.4, 18.5, 21.0, 19.3]

print(len(temperaturen))

for t in temperaturen: 
    print(t)

print(ist_warm)

for t in temperaturen:
    print("Messwert:")
    print(t)



sum = 0

for t in temperaturen: 
    sum += t 
print(sum) 

nenner = len(temperaturen)

avg = sum / nenner

print(avg)

for t in temperaturen:
    print(t)
    if t > 20: 
        break  


for t in temperaturen: 
    if t > 20: 
        print(t)


anzahl = 0 

for t in temperaturen:
   
    if t > 20:
        anzahl += 1
print(anzahl)
