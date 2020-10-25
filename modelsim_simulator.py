import os
import subprocess
import circuit
class ModelSim_Simulator():
	def __init__(self):
		self.input_file_name=''
		self.circuit_name=''

	def __del__(self):
		pass

	def testbench_generator(self, circuit, input_file_name):
		#create the gold folder
		self.input_file_name=input_file_name
		self.circuit_name=circuit.c_name
		dir = './' + circuit.c_name + '/'
		if os.path.exists(dir+'/gold') == False:
			os.mkdir(dir+'/gold')
		#input file are stored in input folder
		#check number of input test patterns
		fr=open(dir+'/input'+input_file_name, mode='r')
		line_list=fr.readlines()
		number_of_test_patterns=len(line_list)-1
		fr.close()

		fw = open(dir + str(circuit.c_name) + "_tb.v", mode='w')
		fw.write("`timescale 1ns/1ns" + "\n")
		fw.write('module ' + str(circuit.c_name) + "_tb;" + '\n')
		fw.write("integer fi, fo;\n")
		fw.write('integer statusI;\n')
		fw.write('integer in_name;\n')
		fw.write('reg in [0:' + str(len(circuit.PI)-1) + '];\n')
		fw.write('wire out [0:' + str(len(circuit.PO) - 1) + '];\n')
		fw.write('reg clk;\n')
		fw.write('\n')
		fw.write(str(circuit.c_name) + ' u_' + str(circuit.c_name) + ' (')
		in_index = 0
		for pi in circuit.PI:
			fw.write('.' + pi.name + '(in[' + str(in_index) + ']),')
			in_index += 1
		out_index = 0
		for po in circuit.PO:
			fw.write('.' + po.name + '(out[' + str(out_index) + '])')
			if out_index != len(circuit.PO)-1:
				fw.write(',')
				out_index += 1
			else:
				fw.write(');\n')

		fw.write('initial begin\n')
		fw.write('\tfi = $fopen("./input/'+input_file_name+'","r");\n')
		fw.write('\tstatusI = $fscanf(fi,"')
		for j in range(len(circuit.PI)):
			fw.write('%s')
			if j != len(circuit.PI) - 1:
				fw.write(',')
			else:
				fw.write('\\n",')
		for j in range(len(circuit.PI)):
			fw.write('in[' + str(j) + ']')
			if j != len(circuit.PI) - 1:
				fw.write(',')
			else:
				fw.write(');\n')
		fw.write('\t#1\n')

		fw.write('\tfo = $fopen("./gold/golden_' + str(circuit.c_name) + '.txt","w");\n')
		fw.write('\tfo = $fopen("./gold/golden_' + str(circuit.c_name) + '.txt","a");\n')
		fw.write('\t$fwrite(fo,"Inputs: ')
		in_index = 0
		for pi in circuit.PI:
			fw.write(pi.name)
			if in_index != len(circuit.PI) - 1:
				fw.write(',')
				in_index += 1
			else:
				fw.write('\\n");\n')
		fw.write('\t$fwrite(fo,"Outputs: ')
		out_index = 0
		for pi in circuit.PO:
			fw.write(pi.name)
			if out_index != len(circuit.PO) - 1:
				fw.write(',')
				out_index += 1
			else:
				fw.write('\\n");\n')
		for i in range(number_of_test_patterns):
			fw.write('\t//test pattern' + str(i) + '\n')
			fw.write('\tstatusI = $fscanf(fi,"')
			for j in range(len(circuit.PI)):
				fw.write('%h')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(circuit.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t#1\n')
			fw.write('\t$display("')
			for j in range(len(circuit.PI)):
				fw.write('%h')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(circuit.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t$display("')
			out_index = 0
			for po in circuit.PO:
				fw.write(po.name + '=%h')
				if out_index != len(circuit.PO) - 1:
					fw.write(',')
					out_index += 1
				else:
					fw.write('\\n",')
					for j in range(len(circuit.PO)):
						fw.write('out[' + str(j) + ']')
						if j != len(circuit.PO) - 1:
							fw.write(',')
							out_index += 1
						else:
							fw.write(');\n')
			fw.write('\t$fwrite(fo, "Test # = ' + str(i) + '\\n");\n')
			fw.write('\t$fwrite(fo,"')
			for j in range(len(circuit.PI)):
				fw.write('%h')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(circuit.PI)):
				fw.write('in[' + str(j) + ']')
				if j != len(circuit.PI) - 1:
					fw.write(',')
				else:
					fw.write(');\n')
			fw.write('\t$fwrite(fo,"')
			for j in range(len(circuit.PO)):
				fw.write('%h')
				if j != len(circuit.PO) - 1:
					fw.write(',')
				else:
					fw.write('\\n",')
			for j in range(len(circuit.PO)):
				fw.write('out[' + str(j) + ']')
				if j != len(circuit.PO) - 1:
					fw.write(',')
				else:
					fw.write(');\n')


		fw.write('\t$fclose(fi);\n')
		fw.write('\t$fclose(fo);\n')

		fw.write('\t$finish;\n')
		fw.write('end\n')
		fw.write('endmodule\n')
		fw.close()
		#create run.sh
		dir = './' + str(circuit.c_name) + '/'
		fw = open(dir + "run.sh", mode='w')
		fw.write('vsim -c -do do_'+str(circuit.c_name)+'.do\n')
		fw.close()
		#create run.do
		fw = open(dir + 'do_'+str(circuit.c_name)+'.do', mode='w')
		fw.write('vlib work\n')
		fw.write('vmap work work\n')
		fw.write('vlog -work work '+str(circuit.c_name)+'.v\n')
		fw.write('vlog -work work '+str(circuit.c_name)+'_tb.v\n')
		fw.write('onerror {resume}\n')
		fw.write('vsim -novopt work.'+str(circuit.c_name)+'_tb\n')
		fw.write('run -all\n')
		fw.close()

	def modelsim_simulation():
		subprocess.call(['sh', './run.sh'], cwd = './'+ self.circuit_name)

	def check():
		#output file created by our platform
		origin_output_file = open('./'+self.circuit_name+'/output/'+self.circuit_name + '_out.txt', "r+")
		#output file form ModelSim
        new_output_file = open('./'+self.circuit_name+'/gold/golden_'+self.circuit_name + '.txt', "r+")
        number_of_line = 1
        origin_line = origin_output_file.readline()
        new_line = new_output_file.readline()
        flag = 1
        if len(origin_line) == 0:
            print("original file is empty!")
            flag = 0
        if len(new_line) == 0:
            print("new file is empty!")
            flag = 0
        if origin_line is not None and new_line is not None:
            while origin_line:
                if origin_line.lower() != new_line.lower():
                    print('file different! different line is #', number_of_line)
                    flag = 0

                else:
                    flag = 1
                origin_line = origin_output_file.readline()
                new_line = new_output_file.readline()
                number_of_line += 1
        if flag == 1:
            print('result are the same')
        else:
            print("result are not same!")
        origin_output_file.close()
        new_output_file.close()


		