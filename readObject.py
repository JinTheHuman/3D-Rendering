def readObject(obj_file):
  vertices = []
  faces = []
  with open(obj_file, "r") as my_file:
    for line in my_file:
      parts = line.strip().split()

      if not parts:
          continue  # Skip empty lines

      if parts[0] == 'v':
          vertices.append([float(x) for x in parts[1:]])
      elif parts[0] == 'f':
          faces.append([int(x) for x in parts[1:]])  
  
  return vertices, faces