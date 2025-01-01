##### A CLASS TO CALCUATE VARIOUS GUITAR SCALES                         ######
##### NEW SCALES CAN BE ADDED BY ADDING THE INTERVALS TO THE SCALE_DICT ######


import fretboard  

class Guitar:
    
    def __init__(self):
    
        self.notes = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b','c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
    
        self.scale_dict = {
            'maj_scale':[0,2,4,5,7,9,11],
            'min_scale':[0,2,3,5,7,8,10],
            'minpent_scale': [0,3,5,7,10],
            'majpent_scale': [0,2,4,7,9],
            'mixylodian_scale': [0,2,4,5,7,9,10],
            'chromatic': [0,1,2,3,4,5,6,7,8,9,10,11],
            'maj_arp':[0,4,7],
            'min_arp':[0,3,7]
        }

        self.tuning_dict = {
            'standard':['e','a','d','g','b','e'],
            'drop d':['d','a','d','g','b','e'],
            'open g':['d','g','d','g','b','d'],
            'bass':['e','a','d','g'],
            'ukelele':['g','c','e','a']
        }

        self.strings_dict = {
            'standard':6,
            'drop d':6,
            'open g':6,
            'bass':4,
            'ukelele':4
        }
    
    def tuningdef(self,tuning):
        tun_ls = self.tuning_dict[tuning]
        return tun_ls 
     
    def string_num(self,tuning):
        strings = self.strings_dict[tuning]
        return strings

    def scale(self,root,scalelist):
        scale_ls=self.scale_dict[scalelist]
        a=self.notes.index(root)
        note_ls = []
        for i in (scale_ls):
            note_ls.append(self.notes[a+i]) 
        return note_ls
    
    def stringdef(self,root):
        scale_ls=self.scale_dict['chromatic']
        a=self.notes.index(root)
        note_ls = []
        for i in (scale_ls):
            note_ls.append(self.notes[a+i]) 
        return note_ls
    
    def Notes_on_String2(self,root,scalelist,stringnum):
#         print(root,scalelist,stringnum)
        string_ls = self.stringdef(stringnum)
        note_ls = self.scale(root,scalelist)
        fret_ls = []
        for i in note_ls:
            fret_ls.append(string_ls.index(i))
        fret_ls.sort()   
        return fret_ls
    
    def full_fretboard(self,root,scale,tuning):
        count=0
        tun_ls=self.tuningdef(tuning)
        for t in tun_ls:
            count+1
            results=self.Notes_on_String2(root,scale,t)
        return results

    def note_labels(self,root,scale,tuning,count):
        tun_ls=self.tuningdef(tuning)
        for t in tun_ls:
            count = count + 1
            results=self.Notes_on_String2(root,scale,t)
            note_ls = []
            fret_ls = []
            for fret in results:
                offset=self.notes.index(t)+fret  
                fret_ls.append(fret)
                note_ls.append(self.notes[offset])
        return note_ls
    
    def add_markers(self,root,scale,tuning,count):
#         print(tuning)
        tun_ls=self.tuningdef(tuning)
#         print(tun_ls)
        marker_ls = []
        for t in tun_ls:
            count=count+1
            results=self.Notes_on_String2(root,scale,t)
            for r in results:
                offset=self.notes.index(t)+r     
                marker_ls.append([count-1,r,self.notes[offset]])
        return marker_ls
                  
    def draw_fretboard(self,fretlow,frethigh,root,scale,tuning,count,svg_file):
        fb = fretboard.Fretboard(frets=(fretlow,frethigh),strings=self.string_num(tuning), style={'drawing': {'width': 400,
                                                                                'height':500},
                                                                    'marker': {'color': 'black'},})
        marker = self.add_markers(root,scale,tuning,count)
        for m in marker:
            if m[1] >= fretlow:
                if m[2] == root  :
                    fb.add_marker(string=m[0], fret=m[1],label=m[2],color='blue')
                    fb.add_marker(string=m[0], fret=m[1]+12,label=m[2],color='blue')
                else:
                    fb.add_marker(string=m[0], fret=m[1],label=m[2])
                    fb.add_marker(string=m[0], fret=m[1]+12,label=m[2])
        fb.save(svg_file)  
   
    def get_svg_string(self,svg_file):
        
        with open(svg_file, "r") as file:
            svg_string = file.read()
        return svg_string
    
    # def display_svg(self,svg_string):
    #     display(SVG(svg_string))