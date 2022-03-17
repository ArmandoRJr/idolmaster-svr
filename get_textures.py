from pathlib import *
import os
import shutil

#User-set variables
pom_extension = ".lz01"      #In case the extension of your .pom files isn't .pom
neat_folder = True          #Put all images in a singular folder
clean_up_pom = True         #Delete unnecessary organization folders
clean_up_tex = True         #Delete extra texture folders (only works when neat_folder = True)
max_no_of_palettes = 100    #Adjust this to your liking (1-based index)
get_no_of_palettes = 1      #Adjust this to your liking, make it smaller than the max no. of palettes (1-based index)

#Let's get this show on the road
abs_root_path = Path.cwd()
#Copying files into neat folders
if (not os.path.exists("./ci8files")): os.mkdir("./ci8files")
if (not os.path.exists("./ci8files_ext")): os.mkdir("./ci8files_ext")
if (not os.path.exists("./ci4files")): os.mkdir("./ci4files")
if (not os.path.exists("./ci4files_ext")): os.mkdir("./ci4files_ext")
if (not os.path.exists("./unknownfiles")): os.mkdir("./unknownfiles")
for pom_file in abs_root_path.rglob(f"*{pom_extension}"):
    with open(pom_file, "rb") as pom_file_br:
        pom_file_all_bytes = pom_file_br.read()
        if (b'\x50\x4f\x4d\x00' in pom_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(pom_file_all_bytes[4:8], "little")
            width = int.from_bytes(pom_file_all_bytes[8:12], "little")
            image_size_ci8 = height * width
            image_size_ci4 = (height * width) // 2

            #Raw CI8 file, no metadata "found" at end of file
            #0x40 + (0x400 * no. of palettes) + image_size [can hold multiple *palettes*, not textures]
            isci8file = False
            no_of_ci8_palettes = 0
            while(os.path.getsize(pom_file) >= (64 + (no_of_ci8_palettes*1024) + image_size_ci8)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(pom_file) == (64 + (no_of_ci8_palettes*1024) + image_size_ci8)):
                    isci8file = True
                    break
                else: no_of_ci8_palettes += 1
            #CI8 file with metadata "found" at end of file
            #0x40 + (0x400 * no. of palettes) + image_size + (0x10 * no. of palettes) [multiple *palettes*]
            isci8file_ext = False
            no_of_ci8_palettes_ext = 1
            while(os.path.getsize(pom_file) >= (64 + (no_of_ci8_palettes_ext*1024) + image_size_ci8 + (16 * no_of_ci8_palettes_ext))):
                #If filesize matches no. of palettes w/metadata
                if (os.path.getsize(pom_file) == (64 + (no_of_ci8_palettes_ext*1024) + image_size_ci8 + (16 * no_of_ci8_palettes_ext))):
                    isci8file_ext = True
                    break
                else: no_of_ci8_palettes_ext += 1
            #Raw CI4 file, no metadata "found" at end of file
            #0x40 + (0x40 * no. of palettes) + image_size [can hold multiple *palettes*, not textures]
            isci4file = False
            no_of_ci4_palettes = 0
            while(os.path.getsize(pom_file) >= (64 + (no_of_ci4_palettes*64) + image_size_ci4)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(pom_file) == (64 + (no_of_ci4_palettes*64) + image_size_ci4)):
                    isci4file = True
                    break
                else: no_of_ci4_palettes += 1
            #CI8 file with metadata "found" at end of file
            #0x40 + (0x40 * no. of palettes) + image_size + (0x10 * no. of palettes) [multiple *palettes*]
            isci4file_ext = False
            no_of_ci4_palettes_ext = 1
            while(os.path.getsize(pom_file) >= (64 + (no_of_ci4_palettes_ext*64) + image_size_ci4 + (16 * no_of_ci4_palettes_ext))):
                #If filesize matches no. of palettes w/metadata
                if (os.path.getsize(pom_file) == (64 + (no_of_ci4_palettes_ext*64) + image_size_ci4 + (16 * no_of_ci4_palettes_ext))):
                    isci4file_ext = True
                    break
                else: no_of_ci4_palettes_ext += 1
            

            pom_filename = os.path.basename(pom_file_br.name)
            #Raw CI8 file, no extension found at end of file
            if (isci8file): 
                print(f"{pom_filename} is type ci8, with {no_of_ci8_palettes} palette(s) [hopefully]!")
                if (pom_file_all_bytes.count(b'\x2e\x70\x6f\x6d') > 1):
                    #If it has more than one instance of .pom somewhere
                    #This file is fuuucked
                    print("Too many textures! Go back!")
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci8files' / f"flagged-{pom_file.stem}-{no_of_ci8_palettes}p.ci8")
                else: 
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci8files' / f"{pom_file.stem}-{no_of_ci8_palettes}p.ci8")
            #CI8 file with metadata
            elif (isci8file_ext):
                print(f"{pom_filename} is type ci8 with extension, with {no_of_ci8_palettes_ext} palette(s) [hopefully]!")
                if (pom_file_all_bytes.count(b'\x2e\x70\x6f\x6d') > 1):
                    #If it has more than one instance of .pom somewhere
                    #This file is fuuucked
                    print("Too many textures! Go back!")
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci8files_ext' / f"flagged-{pom_file.stem}-{no_of_ci8_palettes_ext}p.ci8ext")
                else: 
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci8files_ext' / f"{pom_file.stem}-{no_of_ci8_palettes_ext}p.ci8ext")
            #Raw CI4 file, no extension found at end of file
            elif (isci4file): 
                print(f"{pom_filename} is type ci4, with {no_of_ci4_palettes} palette(s) [hopefully]!")
                if (pom_file_all_bytes.count(b'\x2e\x70\x6f\x6d') > 1):
                    #If it has more than one instance of .pom somewhere
                    #This file is fuuucked
                    print("Too many textures! Go back!")
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci4files' / f"flagged-{pom_file.stem}-{no_of_ci4_palettes}p.ci4")
                else: 
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci4files' / f"{pom_file.stem}-{no_of_ci4_palettes}p.ci4")
            #CI4 file with metadata
            elif (isci4file_ext):
                print(f"{pom_filename} is type ci4 with extension, with {no_of_ci4_palettes_ext} palette(s) [hopefully]!")
                if (pom_file_all_bytes.count(b'\x2e\x70\x6f\x6d') > 1):
                    #If it has more than one instance of .pom somewhere
                    #This file is fuuucked
                    print("Too many textures! Go back!")
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci4files_ext' / f"flagged-{pom_file.stem}-{no_of_ci4_palettes_ext}p.ci4ext")
                else: 
                    shutil.copy(pom_filename,
                    Path.cwd() / 'ci4files_ext' / f"{pom_file.stem}-{no_of_ci4_palettes_ext}p.ci4ext")
            #Deadass don't know about this file, oh fuck
            else:
                print(f"{pom_filename} is type [unknown] (Ignore this for now)!")
                shutil.copy(pom_filename,
                Path.cwd() / 'unknownfiles' / (pom_file.stem + '.unknown'))

        pom_file_br.close()

#Let's see how many files have a disgusting amount of palettes
no_files_too_big = 0
too_big_filenames = []

#Handling CI8 files with no metadata at end 
if (not os.path.exists("./ci8_textures")): os.mkdir("./ci8_textures")
for ci8_file in abs_root_path.rglob("*.ci8"):
    with open(ci8_file, "rb") as ci8_br:
        ci8_file_all_bytes = ci8_br.read()
        if (b'\x50\x4f\x4d\x00' in ci8_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(ci8_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci8_file_all_bytes[8:12], "little")
            image_size = height * width

            #Count no. of palettes
            no_of_palettes = 0
            while(os.path.getsize(ci8_file) >= (64 + (no_of_palettes*1024) + image_size)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(ci8_file) == (64 + (no_of_palettes*1024) + image_size)):
                    break
                else: no_of_palettes += 1

            #Making sure CI8 file is not too big
            if (no_of_palettes < max_no_of_palettes):
                print(f"Currently examining {os.path.basename(ci8_file.name)}")
                #Getting palettes
                palettes = []
                for i in range(0, no_of_palettes):
                    palettes.append(ci8_file_all_bytes[ 64+(i*1024) : 64+(i*1024)+1024] )
                #Getting image data
                image_data = ci8_file_all_bytes[ 64+(no_of_palettes*1024) : 64+(no_of_palettes*1024)+image_size]

                #Making SVRs
                index = 0
                for palette in palettes[:get_no_of_palettes]:
                    rel_path_ci8_svr = f"./ci8_textures/{ci8_file.stem}-{index}.svr"
                    ci8svr_br = open(rel_path_ci8_svr, "wb")

                    ci8svr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                    ci8svr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                    ci8svr_br.write((1024 + 8 + image_size).to_bytes(4, "little"))                    #Filesize + 8 extra bytes
                    ci8svr_br.write(b'\x09\x6c')                                                            #CI8 flag
                    ci8svr_br.write(b'\x00\x00')                                                            #00 00
                    ci8svr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                    ci8svr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                    ci8svr_br.write(palette)                             #Palette data for CI8 file
                    ci8svr_br.write(image_data)      #Image data for CI8 file
                    ci8svr_br.close()
                    index += 1
            else:
                no_files_too_big += 1
                too_big_filenames.append(ci8_file.stem)

        ci8_br.close()


#Handling CI8 files with metadata at end 
if (not os.path.exists("./ci8ext_textures")): os.mkdir("./ci8ext_textures")
for ci8ext_file in abs_root_path.rglob("*.ci8ext"):
    with open(ci8ext_file, "rb") as ci8ext_br:
        ci8ext_file_all_bytes = ci8ext_br.read()
        if (b'\x50\x4f\x4d\x00' in ci8ext_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(ci8ext_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci8ext_file_all_bytes[8:12], "little")
            image_size = height * width

            #Count no. of palettes
            no_of_palettes = 0
            while(os.path.getsize(ci8ext_file) >= (64 + (no_of_palettes*1024) + image_size) + (no_of_palettes * 16)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(ci8ext_file) == (64 + (no_of_palettes*1024) + image_size + (no_of_palettes * 16))):
                    break
                else: no_of_palettes += 1

            #Making sure CI8(-ext) file is not too big
            if (no_of_palettes < max_no_of_palettes):
                print(f"Currently examining {os.path.basename(ci8ext_file.name)}")
                #Getting palettes
                palettes = []
                for i in range(0, no_of_palettes):
                    palettes.append(ci8ext_file_all_bytes[ 64+(i*1024) : 64+(i*1024)+1024] )
                #Getting image data
                image_data = ci8ext_file_all_bytes[ 64+(no_of_palettes*1024) : 64+(no_of_palettes*1024)+image_size]

                #Making SVRs
                index = 0
                for palette in palettes[:get_no_of_palettes]:
                    rel_path_ci8ext_svr = f"./ci8ext_textures/{ci8ext_file.stem}-{index}.svr"
                    ci8extsvr_br = open(rel_path_ci8ext_svr, "wb")

                    ci8extsvr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                    ci8extsvr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                    ci8extsvr_br.write((1024 + 8 + image_size).to_bytes(4, "little"))                    #Filesize + 8 extra bytes
                    ci8extsvr_br.write(b'\x09\x6c')                                                            #CI8 flag
                    ci8extsvr_br.write(b'\x00\x00')                                                            #00 00
                    ci8extsvr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                    ci8extsvr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                    ci8extsvr_br.write(palette)                             #Palette data for CI8 file
                    ci8extsvr_br.write(image_data)      #Image data for CI8 file
                    ci8extsvr_br.close()
                    index += 1
            else: 
                no_files_too_big += 1
                too_big_filenames.append(ci8ext_file.stem)

        ci8ext_br.close()

#Handling CI4 files with no metadata at end 
if (not os.path.exists("./ci4_textures")): os.mkdir("./ci4_textures")
for ci4_file in abs_root_path.rglob("*.ci4"):
    with open(ci4_file, "rb") as ci4_br:
        ci4_file_all_bytes = ci4_br.read()
        if (b'\x50\x4f\x4d\x00' in ci4_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(ci4_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci4_file_all_bytes[8:12], "little")
            image_size = (height * width) // 2

            #Count no. of palettes
            no_of_palettes = 0
            while(os.path.getsize(ci4_file) >= (64 + (no_of_palettes*64) + image_size)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(ci4_file) == (64 + (no_of_palettes*64) + image_size)):
                    break
                else: no_of_palettes += 1

            #Making sure CI4 file is not too big
            if (no_of_palettes < max_no_of_palettes):
                print(f"Currently examining {os.path.basename(ci4_file.name)}")
                #Getting palettes
                palettes = []
                for i in range(0, no_of_palettes):
                    palettes.append(ci4_file_all_bytes[ 64+(i*64) : 64+(i*64)+64] )
                #Getting image data
                image_data = ci4_file_all_bytes[ 64+(no_of_palettes*64) : 64+(no_of_palettes*64)+image_size]

                #Making SVRs
                index = 0
                for palette in palettes[:get_no_of_palettes]:
                    rel_path_ci4_svr = f"./ci4_textures/{ci4_file.stem}-{index}.svr"
                    ci4svr_br = open(rel_path_ci4_svr, "wb")

                    ci4svr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                    ci4svr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                    ci4svr_br.write((64 + 8 + image_size).to_bytes(4, "little"))                      #Filesize + 8 extra bytes
                    ci4svr_br.write(b'\x09\x68')                                                            #CI4 flag
                    ci4svr_br.write(b'\x00\x00')                                                            #00 00
                    ci4svr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                    ci4svr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                    ci4svr_br.write(palette)                             #Palette data for CI4 file
                    ci4svr_br.write(image_data)      #Image data for CI4 file
                    ci4svr_br.close()
                    index += 1
            else: 
                no_files_too_big += 1
                too_big_filenames.append(ci4_file.stem)

        ci4_br.close()

#Handling CI4 files with metadata at end 
if (not os.path.exists("./ci4ext_textures")): os.mkdir("./ci4ext_textures")
for ci4ext_file in abs_root_path.rglob("*.ci4ext"):
    with open(ci4ext_file, "rb") as ci4ext_br:
        ci4ext_file_all_bytes = ci4ext_br.read()
        if (b'\x50\x4f\x4d\x00' in ci4ext_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(ci4ext_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci4ext_file_all_bytes[8:12], "little")
            image_size = (height * width) // 2

            #Count no. of palettes
            no_of_palettes = 0
            while(os.path.getsize(ci4ext_file) >= (64 + (no_of_palettes*64) + image_size) + (no_of_palettes * 16)):
                #If filesize matches no. of palettes w/no metadata
                if (os.path.getsize(ci4ext_file) == (64 + (no_of_palettes*64) + image_size + (no_of_palettes * 16))):
                    break
                else: no_of_palettes += 1

            #Making sure CI4(-ext) file is not too big
            if (no_of_palettes < max_no_of_palettes):
                print(f"Currently examining {os.path.basename(ci4ext_file.name)}")
                #Getting palettes
                palettes = []
                for i in range(0, no_of_palettes):
                    palettes.append(ci4ext_file_all_bytes[ 64+(i*64) : 64+(i*64)+64] )
                #Getting image data
                image_data = ci4ext_file_all_bytes[ 64+(no_of_palettes*64) : 64+(no_of_palettes*64)+image_size]

                #Making SVRs
                index = 0
                for palette in palettes[:get_no_of_palettes]:
                    rel_path_ci4ext_svr = f"./ci4ext_textures/{ci4ext_file.stem}-{index}.svr"
                    ci4extsvr_br = open(rel_path_ci4ext_svr, "wb")

                    ci4extsvr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                    ci4extsvr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                    ci4extsvr_br.write((64 + 8 + image_size).to_bytes(4, "little"))                    #Filesize + 8 extra bytes
                    ci4extsvr_br.write(b'\x09\x68')                                                            #CI4 flag
                    ci4extsvr_br.write(b'\x00\x00')                                                            #00 00
                    ci4extsvr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                    ci4extsvr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                    ci4extsvr_br.write(palette)                             #Palette data for CI4 file
                    ci4extsvr_br.write(image_data)      #Image data for CI4 file
                    ci4extsvr_br.close()
                    index += 1
            else: 
                no_files_too_big += 1
                too_big_filenames.append(ci4ext_file.stem)

        ci4ext_br.close()

#THIS IS ABOUT TO BE A GIIIIIIIIIANT MESS
#Handling unknown files...by goddamn bruteforcing it 
if (not os.path.exists("./unknown_textures")): os.mkdir("./unknown_textures")
for unknown_file in abs_root_path.rglob("*.unknown"):
    with open(unknown_file, "rb") as unknown_br:
        unknown_file_all_bytes = unknown_br.read()
        if (b'\x50\x4f\x4d\x00' in unknown_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(unknown_file_all_bytes[4:8], "little")
            width = int.from_bytes(unknown_file_all_bytes[8:12], "little")
            
            #Yes, we're trying this dumb tecnique
            dotpomact_index = 0
            folder_name = ""
            if (b'\x2e\x61\x63\x74' in unknown_file_all_bytes
                or b'\x2e\x70\x6f\x6d' in unknown_file_all_bytes):                  #.act or .pom in file...somewhere
                if b'\x2e\x61\x63\x74' in unknown_file_all_bytes:
                    dotpomact_index = unknown_file_all_bytes.index(b'\x2e\x61\x63\x74')     #Get .act info
                    folder_name = "act_search"
                elif b'\x2e\x70\x6f\x6d' in unknown_file_all_bytes:
                    dotpomact_index = unknown_file_all_bytes.index(b'\x2e\x70\x6f\x6d')     #or get .pom info
                    folder_name = "pom_search"
                
                #CI4 size
                image_size = (width * height) // 2
                almost_full_size = dotpomact_index - (dotpomact_index % 16)     #Remove everything after .act/.pom
                extra_bytes = (almost_full_size - (64 + image_size)) % 64       #Extra bytes prior to .act/.pom (i.e. .pom file metadata)
                total_size = almost_full_size - extra_bytes                     #Total filesize
                no_of_palettes = (total_size - 64 - image_size) // 64           #Theoretical no. of palettes
            
                if (not os.path.exists(f"./unknown_textures/ci4")): 
                    os.mkdir(f"./unknown_textures/ci4")
                if(no_of_palettes < max_no_of_palettes):                                       #Don't run this shit if too big
                    print(f"Currently examining {os.path.basename(unknown_file.name)}")
                    palettes = []
                    for i in range(0, no_of_palettes):
                        palettes.append(unknown_file_all_bytes[ 64+(i*64) : 64+(i*64)+64] )
                    image_data = unknown_file_all_bytes[ 64+(no_of_palettes*64) : 64+(no_of_palettes*64)+image_size]

                    if (not os.path.exists(f"./unknown_textures/ci4/{folder_name}")): 
                        os.mkdir(f"./unknown_textures/ci4/{folder_name}")
                    index = 0
                    for palette in palettes[:get_no_of_palettes]:
                        rel_path_unknown_svr = f"./unknown_textures/ci4/{folder_name}/{unknown_file.stem}-{index}.svr"
                        unknownsvr_br = open(rel_path_unknown_svr, "wb")

                        unknownsvr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                        unknownsvr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                        unknownsvr_br.write((64 + 8 + image_size).to_bytes(4, "little"))                            #Filesize + 8 extra bytes
                        unknownsvr_br.write(b'\x09\x68')                                                            #CI4 flag
                        unknownsvr_br.write(b'\x00\x00')                                                            #00 00
                        unknownsvr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                        unknownsvr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                        unknownsvr_br.write(palette)                             #Palette data for CI4 file
                        unknownsvr_br.write(image_data)                          #Image data for CI4 file
                        unknownsvr_br.close()
                        index += 1
                else: 
                    no_files_too_big += 1
                    too_big_filenames.append(unknown_file.stem)
                    

                #CI8 size
                image_size = (width * height)
                almost_full_size = dotpomact_index - (dotpomact_index % 16)     #Remove everything after .act/.pom
                extra_bytes = (almost_full_size - (64 + image_size)) % 1024       #Extra bytes prior to .act/.pom (i.e. .pom file metadata)
                total_size = almost_full_size - extra_bytes                     #Total filesize
                no_of_palettes = (total_size - 64 - image_size) // 1024           #Theoretical no. of palettes
            
                if (not os.path.exists(f"./unknown_textures/ci8")): 
                    os.mkdir(f"./unknown_textures/ci8")
                if(no_of_palettes < max_no_of_palettes):                                       #Don't run this shit if too big
                    print(f"Currently examining {os.path.basename(unknown_file.name)}")
                    palettes = []
                    for i in range(0, no_of_palettes):
                        palettes.append(unknown_file_all_bytes[ 64+(i*1024) : 64+(i*1024)+1024] )
                    image_data = unknown_file_all_bytes[ 64+(no_of_palettes*1024) : 64+(no_of_palettes*1024)+image_size]

                    if (not os.path.exists(f"./unknown_textures/ci8/{folder_name}/")): 
                        os.mkdir(f"./unknown_textures/ci8/{folder_name}/")
                    index = 0
                    for palette in palettes[:get_no_of_palettes]:
                        rel_path_unknown_svr = f"./unknown_textures/ci8/{folder_name}/{unknown_file.stem}-{index}.svr"
                        unknownsvr_br = open(rel_path_unknown_svr, "wb")

                        unknownsvr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                        unknownsvr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                        unknownsvr_br.write((1024 + 8 + image_size).to_bytes(4, "little"))                          #Filesize + 8 extra bytes
                        unknownsvr_br.write(b'\x09\x6c')                                                            #CI8 flag
                        unknownsvr_br.write(b'\x00\x00')                                                            #00 00
                        unknownsvr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                        unknownsvr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                        unknownsvr_br.write(palette)                             #Palette data for CI8 file
                        unknownsvr_br.write(image_data)                          #Image data for CI8 file
                        unknownsvr_br.close()
                        index += 1
                else: 
                    no_files_too_big += 1
                    too_big_filenames.append(unknown_file.stem)
        unknown_br.close()
#GIIIIIIIIIANT MESS ENDS HERE

print(f"We skipped files {no_files_too_big} times (but not exactly {no_files_too_big} files).")
print(too_big_filenames)

if (neat_folder):
    print("Moving everything to a neat folder, please wait warmly.")
    print("If I crash, delete your all_textures folder first and try me again.")
    if (not os.path.exists("./all_textures")): os.mkdir("./all_textures")
    for svr_file in abs_root_path.rglob("*.svr"):
        svr_filename = os.path.basename(svr_file.name)
        shutil.copy(svr_file,
        Path.cwd() / 'all_textures' / svr_filename)
    print("File transfers done.")

    if (clean_up_pom):
        print("Cleaning up extra texture folders...")
        if (os.path.exists("./ci4_textures")): shutil.rmtree("./ci4_textures")
        if (os.path.exists("./ci4ext_textures")): shutil.rmtree("./ci4ext_textures")
        if (os.path.exists("./ci8_textures")): shutil.rmtree("./ci8_textures")
        if (os.path.exists("./ci8ext_textures")): shutil.rmtree("./ci8ext_textures")
        if (os.path.exists("./unknown_textures")): shutil.rmtree("./unknown_textures")
        print("Extra folders cleaned up.")

print("Cleaning up unnecessary folders...")
if (os.path.exists("./ci8files")): shutil.rmtree("./ci8files")
if (os.path.exists("./ci8files_ext")): shutil.rmtree("./ci8files_ext")
if (os.path.exists("./ci4files")): shutil.rmtree("./ci4files")
if (os.path.exists("./ci4files_ext")): shutil.rmtree("./ci4files_ext")
if (os.path.exists("./unknownfiles")): shutil.rmtree("./unknownfiles")
print("Unnecessary folders cleaned up.")

print("All done.")