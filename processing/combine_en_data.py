def preprocess_conll(data):

    """
    Quick preprocessing on the CONLL data so it can be combined
    with the Emerging Entities data (which doesn't need any
    preprocessing).

    Takes `data`, which is a list of strings read in from
    a CONLL data file.
    """

    # Remove DOCSTART lines to make CONLL data consistent
    # with the Emerging Entities dataset
    data = [line for line in data if 'DOCSTART' not in line]

    # Add appropriate tabbing and spacing to match EE data
    data = ['\t'.join([line.split()[0], line.split()[3]]) + '\n'
            if line != '\n'
            else line
            for line in data]

    return data

def create_combined_en_dataset(dataset_path_list, combined_path):

    """
    Takes a dataset_path_list of the two English datasets (can be edited
    to accommodate more datasets later), and a combined_path, which
    is a path string describing where to save the data.

    Combines the two English datasets such that they have the same formatting;
    specifically, each line should look like this: TOKEN\tLABEL\n.
    See example below.
     ['EU\tB-ORG\n',
     'rejects\tO\n',
     'German\tB-MISC\n',
     'call\tO\n',
     'to\tO\n',
     'boycott\tO\n',
     'British\tB-MISC\n',
     'lamb\tO\n',
     '.\tO\n',
     '\n', ...]
    """

    for path in dataset_path_list:
        # indicates that these are the CONLL files
        conll_paths = ['test.txt', 'train.txt', 'valid.txt']
        if path in ['../data/en/CONLL2003/' + p for p in conll_paths]:
            with open(path, 'r') as conll:
                conll_data = preprocess_conll(conll.readlines())

        else:
            with open(path, 'r') as ee:
                ee_data = ee.readlines()

    # Combine the two datasets
    ee_data.extend(conll_data)

    # Write out to specified path
    with open(combined_path, 'w+') as new:
        new.writelines(ee_data)

    # Print success message
    print('Combined {} and saved new dataset to {}.'
         .format(dataset_path_list, combined_path))

    return None


if __name__ == '__main__':

    conll_path = '../data/en/CONLL2003/'
    ee_path = '../data/en/emerging_entities_17/'
    combined_path = '../data/en/combined/'

    # Training set
    create_combined_en_dataset([conll_path + 'train.txt',
                                ee_path + 'wnut17train.conll'],
                                combined_path + 'train_combined.txt')

    # Validation set
    create_combined_en_dataset([conll_path + 'valid.txt',
                                ee_path + 'emerging.dev.conll'],
                                combined_path + 'dev_combined.txt')

    # Test set
    create_combined_en_dataset([conll_path + 'test.txt',
                                ee_path + 'emerging.test.annotated'],
                                combined_path + 'test_combined.txt')
