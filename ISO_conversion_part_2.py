for i in range(len(t)):
    try:
        int(t[i])
        if index == -1:
            index = i
            continue    
    except:
        if index != -1:
            total += int(t[index:i]) * time_dict[t[i]]
            index = -1

prompt = ""
if "H" in t: prompt += t[t.find("T")+1:t.find("H")] + " hours"
if prompt and "M" in t: prompt +=  " and " + t[t.find("H")+1:t.find("M")] + " minutes"
elif "M" in t: prompt += t[t.find("T")+1:t.find("M")] + " minutes"
elif "M" in t and "S" in t: prompt += " and " + t[t.find("M")+1:t.find("S")] + " seconds"
if "H" in t and "S" in t: prompt += " and " + t[t.find("H")+1:t.find("S")] + " seconds"
elif "S" in t: prompt += t[t.find("T")+1:t.find("S")] + " seconds"