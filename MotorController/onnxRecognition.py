import onnx

# Load ONNX model
#Change to model source
model = onnx.load("./eyesModelOld.onnx")

# Get the expected inputs
inputs = model.graph.input

# Print the details of each input
print("Inputs:")
for input in inputs:
    name = input.name
    shape = [dim.dim_value for dim in input.type.tensor_type.shape.dim]
    data_type = input.type.tensor_type.elem_type

    print(f"Input name: {name}")
    print(f"Shape: {shape}")
    print(f"Data type: {data_type}")
    print()

print("\n\n\n")
outputs = model.graph.output

# Print the details of each output
print("Outputs:")
for output in outputs:
    name = output.name
    shape = [dim.dim_value for dim in output.type.tensor_type.shape.dim]
    data_type = output.type.tensor_type.elem_type

    print(f"Output name: {name}")
    print(f"Shape: {shape}")
    print(f"Data type: {data_type}")
    print()


"""
Inputs:

Numpy Array format
s
obs = [1,220]
where [batch - self defined, Array]
Array index:
0 - Flag: 0 is, 1 is not camera 1
1 - X position normalized 0 - 1 camera 1
2 - Y position normalized 0 - 1 camera 1
3 - Flag: 0 is, 1 is not camera 2
4 - X position normalized 0 - 1 camera 2
5 - Y position normalized 0 - 1 camera 2
6-219 = 0

action_mask = [0,12]
where [batch - self defined, Array]
Array index
0, 3, 6, 9 = 0
1, 4, 7, 10 = 1
2, 5, 8, 11 = 2

recurrent_in = [0, 1, 64]
where [batch - self defined, x, x]
x = 0
recurrent_in = recurrent_out



Outputs:

deterministic_discrete_actions = [1,4]
where [Single array output, ]
0 - X movement camera 1 
1 - Y movement camera 1
2 - X movement camera 2 
3 - Y movement camera 2

"""
