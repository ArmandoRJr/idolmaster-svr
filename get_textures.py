from pathlib import *
import os
import shutil

abs_root_path = Path.cwd()
#Copying files into neat folders
if (not os.path.exists("./ci8files")): os.mkdir("./ci8files")
if (not os.path.exists("./ci8files_ext")): os.mkdir("./ci8files_ext")
if (not os.path.exists("./ci4files")): os.mkdir("./ci4files")
for pom_file in abs_root_path.rglob("*pom"):
    with open(pom_file, "rb") as pom_file_br:
        pom_file_all_bytes = pom_file_br.read()
        if (b'\x50\x4f\x4d\x00' in pom_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(pom_file_all_bytes[4:8], "little")
            width = int.from_bytes(pom_file_all_bytes[8:12], "little")
            image_size = height * width

            #0x40 + 0x400 + image_size
            #OR 0x40 + 0x400 + image_size + .pom filename at end
            isci8palette = (os.path.getsize(pom_file_br.name) == (64 + 1024 + image_size))
            isci8palette_ext = (os.path.getsize(pom_file_br.name) == (64 + 1024 + image_size + 16))
            #Raw CI8 file, no extension found at end of file
            if (isci8palette): 
                print(f"{os.path.basename(pom_file_br.name)} is type ci8!")
                shutil.copy(os.path.basename(pom_file_br.name),
                Path.cwd() / 'ci8files' / (pom_file.stem + '.ci8'))
            #CI8 file with metadata
            elif (isci8palette_ext):
                print(f"{os.path.basename(pom_file_br.name)} is type ci8 with extension!")
                shutil.copy(os.path.basename(pom_file_br.name),
                Path.cwd() / 'ci8files_ext' / (pom_file.stem + '.ci8ext'))
            #CI4 file (in theory)
            else:
                print(f"{os.path.basename(pom_file_br.name)} is type ci4!")
                shutil.copy(os.path.basename(pom_file_br.name),
                Path.cwd() / 'ci4files' / (pom_file.stem + '.ci4'))

        pom_file_br.close()

#Handling CI8 files with no metadata at end 
if (not os.path.exists("./ci8_textures")): os.mkdir("./ci8_textures")
for ci8_file in abs_root_path.rglob("*.ci8"):
    with open(ci8_file, "rb") as ci8_br:
        ci8_file_all_bytes = ci8_br.read()
        if (b'\x50\x4f\x4d\x00' in ci8_file_all_bytes[:4]): #If POM magic available
            print(f"Currently examining {os.path.basename(ci8_file.name)}")
            height = int.from_bytes(ci8_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci8_file_all_bytes[8:12], "little")
            image_size = height * width
            
            rel_path_ci8_svr = f"./ci8_textures/{ci8_file.stem}-0.svr"
            ci8svr_br = open(rel_path_ci8_svr, "wb")

            ci8svr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
            ci8svr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
            ci8svr_br.write((1024 + 8 + width * height).to_bytes(4, "little"))                      #Filesize + 8 extra bytes
            ci8svr_br.write(b'\x09\x6c')                                                            #CI8 flag
            ci8svr_br.write(b'\x00\x00')                                                            #00 00
            ci8svr_br.write(width.to_bytes(2, "little"))                                            #In16 width
            ci8svr_br.write(height.to_bytes(2, "little"))                                           #In16 height
            ci8svr_br.write(ci8_file_all_bytes[64:1024+64])                             #Palette data for CI8 file
            ci8svr_br.write(ci8_file_all_bytes[1024+64: 1024+64+(width * height)])      #Image data for CI8 file
            ci8svr_br.close()

        ci8_br.close()

#Handling CI8 files with  metadata at end 
if (not os.path.exists("./ci8ext_textures")): os.mkdir("./ci8ext_textures")
for ci8ext_file in abs_root_path.rglob("*.ci8ext"):
    with open(ci8ext_file, "rb") as ci8ext_br:
        ci8ext_file_all_bytes = ci8ext_br.read()
        if (b'\x50\x4f\x4d\x00' in ci8ext_file_all_bytes[:4]): #If POM magic available
            print(f"Currently examining {os.path.basename(ci8ext_file.name)}")
            height = int.from_bytes(ci8ext_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci8ext_file_all_bytes[8:12], "little")
            image_size = height * width
            
            rel_path_ci8ext_svr = f"./ci8ext_textures/{ci8ext_file.stem}-0.svr"
            ci8svextr_br = open(rel_path_ci8ext_svr, "wb")

            ci8svextr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
            ci8svextr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
            ci8svextr_br.write((1024 + 8 + width * height).to_bytes(4, "little"))                      #Filesize + 8 extra bytes
            ci8svextr_br.write(b'\x09\x6c')                                                            #CI8 flag
            ci8svextr_br.write(b'\x00\x00')                                                            #00 00
            ci8svextr_br.write(width.to_bytes(2, "little"))                                            #In16 width
            ci8svextr_br.write(height.to_bytes(2, "little"))                                           #In16 height
            ci8svextr_br.write(ci8ext_file_all_bytes[64:1024+64])                             #Palette data for CI8 file
            ci8svextr_br.write(ci8ext_file_all_bytes[1024+64: 1024+64+(width * height)])      #Image data for CI8 file
            ci8svextr_br.close()

        ci8ext_br.close()


files_too_big = 0
too_big_filenames = []
#Handling CI4 files in general
if (not os.path.exists("./ci4_textures")): os.mkdir("./ci4_textures")
for ci4_file in abs_root_path.rglob("*.ci4"):
    with open(ci4_file, "rb") as ci4_br:
        ci4_file_all_bytes = ci4_br.read()
        if (b'\x50\x4f\x4d\x00' in ci4_file_all_bytes[:4]): #If POM magic available
            height = int.from_bytes(ci4_file_all_bytes[4:8], "little")
            width = int.from_bytes(ci4_file_all_bytes[8:12], "little")
            image_size = (height * width) // 2

            
            pom_act_trick_worked = False        #Yes, this is a wack flag lmao
            if (b'\x2e\x61\x63\x74' in ci4_file_all_bytes
                or b'\x2e\x70\x6f\x6d' in ci4_file_all_bytes):                  #.act or .pom in file...somewhere
                
                dotpomact_index = 0
                folder_name = ""
                if b'\x2e\x61\x63\x74' in ci4_file_all_bytes:
                    dotpomact_index = ci4_file_all_bytes.index(b'\x2e\x61\x63\x74')     #Get .act info
                    folder_name = "act_search"
                elif b'\x2e\x70\x6f\x6d' in ci4_file_all_bytes:
                    dotpomact_index = ci4_file_all_bytes.index(b'\x2e\x70\x6f\x6d')     #or get .pom info
                    folder_name = "pom_search"

                almost_full_size = dotpomact_index - (dotpomact_index % 16)     #Remove everything after .act/.pom
                extra_bytes = (almost_full_size - (64 + image_size)) % 64       #Extra bytes prior to .act/.pom (i.e. .pom file metadata)
                total_size = almost_full_size - extra_bytes                     #Total filesize
                no_of_palettes = (total_size - 64 - image_size) // 64           #Theoretical no. of palettes
                #print(f"{total_size} is the final siiiize!")
                #print(f"The image_size is {image_size}")
                #print(f"and it has {no_of_palettes} palettes!")

                if(no_of_palettes < 100):                                       #Don't run this shit if too big
                    print(f"Currently examining {os.path.basename(ci4_file.name)}")
                    palettes = []
                    for i in range(0, no_of_palettes):
                        palettes.append(ci4_file_all_bytes[ 64+(i*64) : 64+(i*64)+64] )
                    image_data = ci4_file_all_bytes[ 64+(no_of_palettes*64) : 64+(no_of_palettes*64)+image_size]

                    if (not os.path.exists(f"./ci4_textures/{folder_name}/")): 
                        os.mkdir(f"./ci4_textures/{folder_name}/")
                    index = 0
                    for palette in palettes:
                        rel_path_ci4_svr = f"./ci4_textures/{folder_name}/{ci4_file.stem}-{index}.svr"
                        ci4svr_br = open(rel_path_ci4_svr, "wb")

                        ci4svr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                        ci4svr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                        ci4svr_br.write((64 + 8 + image_size).to_bytes(4, "little"))                            #Filesize + 8 extra bytes
                        ci4svr_br.write(b'\x09\x68')                                                            #CI4 flag
                        ci4svr_br.write(b'\x00\x00')                                                            #00 00
                        ci4svr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                        ci4svr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                        ci4svr_br.write(palette)                             #Palette data for CI4 file
                        ci4svr_br.write(image_data)                          #Image data for CI4 file
                        ci4svr_br.close()
                        index += 1
                    pom_act_trick_worked = True
                #else: print("DONT WORK WITH THIS FILE!")

            
            if (not pom_act_trick_worked):
                no_of_palettes = 0
                while(os.path.getsize(ci4_br.name) >= (64 + (no_of_palettes*64) + image_size)):
                    if (os.path.getsize(ci4_br.name) == (64 + (no_of_palettes*80) + image_size)         #If filesize matches no. of palettes w/metadata
                        or os.path.getsize(ci4_br.name) == (64 + (no_of_palettes*64) + image_size)):    #or without metadata
                        if (no_of_palettes < 100):                  #Don't run this shit if too big
                            print(f"Currently examining {os.path.basename(ci4_file.name)}")
                            folder_name = ""
                            if (os.path.getsize(ci4_br.name) == (64 + (no_of_palettes*80) + image_size)):
                                folder_name = "metadata_available"
                            elif (os.path.getsize(ci4_br.name) == (64 + (no_of_palettes*64) + image_size)):
                                folder_name = "no_metadata_available"

                            palettes = []
                            for i in range(0, no_of_palettes):
                                palettes.append(ci4_file_all_bytes[ 64+(i*64) : 64+(i*64)+64] )
                            image_data = ci4_file_all_bytes[ 64+(no_of_palettes*64) : 64+(no_of_palettes*64)+image_size]

                            if (not os.path.exists(f"./ci4_textures/{folder_name}/")): 
                                os.mkdir(f"./ci4_textures/{folder_name}/")
                            index = 0
                            for palette in palettes:
                                rel_path_ci4_svr = f"./ci4_textures/{folder_name}/{ci4_file.stem}-{index}.svr"
                                ci4svr_br = open(rel_path_ci4_svr, "wb")

                                ci4svr_br.write(b'\x47\x42\x49\x58\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    #Start of SVR header
                                ci4svr_br.write(b'\x50\x56\x52\x54')                                                    #PVRT
                                ci4svr_br.write((64 + 8 + image_size).to_bytes(4, "little"))                            #Filesize + 8 extra bytes
                                ci4svr_br.write(b'\x09\x68')                                                            #CI4 flag
                                ci4svr_br.write(b'\x00\x00')                                                            #00 00
                                ci4svr_br.write(width.to_bytes(2, "little"))                                            #In16 width
                                ci4svr_br.write(height.to_bytes(2, "little"))                                           #In16 height
                                ci4svr_br.write(palette)                             #Palette data for CI4 file
                                ci4svr_br.write(image_data)                          #Image data for CI4 file
                                ci4svr_br.close()
                                index += 1
                            break
                        else: 
                            files_too_big += 1
                            too_big_filenames.append(ci4_file.stem)

                        
                    no_of_palettes += 1
            
                
                    

        ci4_br.close()

print(f"We fucked up {files_too_big} times.")
print(too_big_filenames)