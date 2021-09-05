"""
Creates a list of tubes required from a BOM list, with the lengths to be cut from each tube.
author: Ben Van Raemdonck
date: 16/06/2021
"""
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def cut_tubes(component, bom_list_path, l_max=6000, use_size=True, t_saw=3):
    """
    Creates a list of tubes required from a BOM list, with the lengths to be cut from each tube.
    Creates a txt file with the result.
    component (str): Component name
    bom_list_path (str): name of BOM list excel file
    l_max (int): standard tube length
    use_size (bool): use columns 'Size' and 'Length', otherwise use 'Diameter', 'Thickness', and 'Length'
    t_saw (float): saw blade thickness
    """
    if use_size:
        bom = pd.read_excel(bom_list_path, header=1, usecols=['Component', 'Quantity', 'Length', 'Size'])
        bom = bom[bom['Component'] == component]
        sizes = list(set(bom['Size']))
    else:
        bom = pd.read_excel(bom_list_path, header=1,
                            usecols=['Component', 'Quantity', 'Length', 'Diameter', 'Thickness'])
        bom = bom[bom['Component'] == component]
        sizes = []
        for d, t in zip(bom['Diameter'], bom['Thickness']):
            if [d, t] not in sizes:
                sizes.append([d, t])
    all_tubes = {}

    for size in sizes:
        if use_size:
            b = bom[bom['Size'] == size].copy()  # bom list with same tube size
        else:
            b = bom[(bom['Diameter'] == size[0]) & (bom['Thickness'] == size[1])].copy()
        tubes_needed = {}
        tubes_length_leftover = {}
        l_remaining = l_max
        i = 1
        while b.any().any():  # while b not empty
            if max(b['Length']) > l_max:  # if length > maximum tube length, decrease length by 6000 and add full tube
                ind = b.loc[b['Length'] == max(b['Length'])].index[0]
                b.loc[ind, 'Length'] -= 6000
                tubes_needed[f'tube {i}'] = [6000]
                i += 1
                continue

            try:
                l_select = max([l for l in b['Length'] if l <= l_remaining])  # pick largest l still able to be cut
                l_remaining -= (l_select + t_saw)

                # subtract quantity by 1 and drop if quantity is 0
                ind = b.loc[b['Length'] == l_select].index[0]
                b.loc[ind, 'Quantity'] -= 1
                if b.loc[ind, 'Quantity'] == 0:
                    b = b.drop(ind)

                # add to tubes_needed
                if f'tube {i}' in tubes_needed:
                    tubes_needed[f'tube {i}'].append(l_select)
                else:
                    tubes_needed[f'tube {i}'] = [l_select]
            except ValueError:  # no fitting l remaining --> new tube
                tubes_length_leftover[f'tube {i}'] = l_remaining + t_saw
                l_remaining = l_max
                i += 1
        tubes_length_leftover[f'tube {i}'] = l_remaining + t_saw

        if use_size:
            all_tubes[size] = [tubes_needed, tubes_length_leftover]
        else:
            all_tubes[f'D {size[0]}, t {size[1]}'] = [tubes_needed, tubes_length_leftover]

    # create txt file
    f = open(f'{bom_list_path[:-5]} - cut tubes.txt', 'a')
    write_file(f, all_tubes, component)
    f.close()

    # return the amount of tubes required
    return all_tubes


def write_file(file_path, tubes_cut, title):
    """
    writes tubes_cut to the text file defined by file_path
    """
    if tubes_cut:  # if the dict is not empty
        if title == 'EN 10217-7':
            file_path.write(f'\n##### Gelaste ronde buis #####\n')
        else:
            file_path.write(f'\n###### {title} #####\n')
    for tube_size, [tube_dict, leftover_dict] in tubes_cut.items():
        file_path.write(f'{tube_size}:\n')
        for tubenr, tube_list in tube_dict.items():
            file_path.write(f'{tubenr}: {tube_list}, leftover: {leftover_dict[tubenr]} mm\n')
        file_path.write('\n')


if __name__ == '__main__':
    Tk().withdraw()
    bom_path = askopenfilename()
    cut_tubes('Constructiebuis vierkant', bom_path, 6000, True, 3)
    cut_tubes('Rechthoekige buis', bom_path)
    cut_tubes('EN 10217-7', bom_path, use_size=False)  # Gelaste ronde buis
    cut_tubes('HDPE100 Drukbuis', bom_path)
    cut_tubes('PVC Drukbuis', bom_path, 5000)
    cut_tubes('Hoeklijn', bom_path)
    cut_tubes('DIN 976-1A', bom_path, 3000)  # Draadstang
