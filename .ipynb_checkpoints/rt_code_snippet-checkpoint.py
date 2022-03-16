# RT code snippet
events_tmp = events.copy() # making a copy of the events structure so we don't fiddle with the original structure
rt = np.zeros([np.shape(events_tmp)[0],2]) # creating an rt-structure with zeros, same length as events and 2 columns
for idx, line in enumerate(events_tmp): # iterating over each line in the events structure
    if any(line[2] == [101,102,111,112]): # picking out only the correct-response lines
        rt[idx] = (line[2],line[0]-events_tmp[idx-1,0]) # subtracting the timestamps of the preceding image from the from that of the response
pure_rt = rt[np.nonzero(rt[:,0]),][0] # creating a structure only with response times (i.e. no "blank" lines for all the other triggers from word, image, etc.)
mean_rt = [(x, np.mean(pure_rt[pure_rt[:,0]==x,1]), 
                    np.std(pure_rt[pure_rt[:,0]==x,1])) 
                   for x in np.unique(pure_rt[:,0])] # calculating the mean and standard deviation of the rt for each unique trigger value in pure_rt (using list comprehension)
[print("{}: {:5.2f} (±{:5.2f}) ms\n".format(list(event_id.keys())[list(event_id.values()).index(i)],
                                            j,k)) for i,j,k in mean_rt] # printing those values (using list comprehension)

image_rt = np.concatenate(([events_tmp[np.nonzero(rt[:,0])[0]-1,2]], [rt[np.nonzero(rt[:,0]),1][0]]), axis=0).T # concatenating image-triggers with the relevant rts
mean_image_rt = [(x, np.mean(image_rt[image_rt[:,0]==x,1]), 
                  np.std(image_rt[image_rt[:,0]==x,1])) 
                 for x in np.unique(image_rt[:,0])] # calculating the mean and standard deviation of the rt for each unique trigger value in image_rt (should be identical to the response-categories
[print("{}: {:5.2f} (±{:5.2f}) ms\n".format(list(event_id.keys())[list(event_id.values()).index(i)],
                                            j,k)) for i,j,k in mean_image_rt] # printing those values