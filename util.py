import os
#import logging

#log_format = "[%(asctime)s: %(levelname)s/%(funcName)s] %(message)s"
#logging.basicConfig(format=log_format, level=logging.INFO)

# figure out dir of input data under work dir
def get_input_dir_path(workDirPath):

    ## load _context.json if it exists
    #ctx = {}
    #ctx_file = "_context.json"
    #if os.path.exists(ctx_file):
    #    with open(ctx_file) as f:
    #        ctx = json.load(f)
    #logging.info("ctx: {}".format(json.dumps(ctx, indent=4)))

    # get SLC stack directory
    found = None
    for x in os.listdir(workDirPath):
        if not os.path.isdir(os.path.join(workDirPath, x)):
            continue
        if x.startswith("coregistered_slcs"):
            found = x
            break
    #print(found)
    mergedFullPath = None
    if found != None:
        mergedFullPath = os.path.join(workDirPath, found, "merged")
    #print("merged full path: {}".format(mergedFullPath))

    return mergedFullPath

def get_output_dir_path(workDirPath):
    #outputDirPath = './output'
    outputDirPath = './s1-gcov'
    return outputDirPath


from netCDF4 import Dataset

class Netcdf4CreatorException(Exception):
    pass

class Netcdf4Creator:

    def __init__(self, outputPath=None):
        if outputPath is None:
            raise Netcdf4CreatorException("No output path given")
        self.rootGroup = Dataset(outputPath, "w", format="NETCDF4")

    def add_2d_array(self, groupFullName, varName, varType, varShape, varValue):
        group = self.rootGroup.createGroup(groupFullName)
        dim0 = group.createDimension("dim0", varShape[0])
        dim1 = group.createDimension("dim1", varShape[1])
        var = group.createVariable(varName, varType, ("dim0", "dim1"))
        print(var)
        var[:] = varValue

    def close(self):
        self.rootGroup.close()

def main():

    workDirPath = "."

    inputDirPath = get_input_dir_path(workDirPath)
    print(inputDirPath)
    outputDirPath = get_output_dir_path(workDirPath)
    print(outputDirPath)

if __name__ == "__main__":
    main()
