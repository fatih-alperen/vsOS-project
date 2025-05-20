#include <stdio.h>
#include <stdint.h>


int main(int argc, char* argv[]){

	size_t MEM_SIZE = 512*1024;
	size_t RUN_LIMIT = 30;
	uint32_t PC = 0;
	uint32_t R1, R2;
	uint32_t memory[MEM_SIZE];
	FILE *disk = fopen("disk.img", "rb");
	if(disk == NULL){
		perror("Error opening file");
		return 1;
	}
	size_t elements_read = fread(memory, sizeof(uint32_t), MEM_SIZE, disk);
	if (ferror(disk)){
		perror("Error reading file");
		fclose(disk);
		return 1;
	}

	fclose(disk);

	printf("File read successfull!\n");

	//main loop, run until haltcode
	//haltcode is the jump instruction that points to itself

	int halt = 0;
	while(!halt && PC < RUN_LIMIT){
		uint32_t instruction = memory[PC];
		uint32_t opcode = (instruction >> 29) & 0b111;
		uint32_t i_flag = (instruction >> 28) & 1;
		uint32_t A = (instruction >> 14) & 0x3FFF;
		uint32_t B = (instruction) & 0x3FFF;

		uint32_t R1 = memory[A];
		uint32_t R2 = (i_flag) ? B : memory[B];
		printf("PC: %d, instruction: %d\n", PC, instruction);

		switch(opcode){
		
			case 0b000:
				printf("ADD");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = R1+R2;
				++PC;
				break;

			case 0b001:
				printf("NAND");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = ~(R1 & R2);
				++PC;
				break;

			case 0b010:
				printf("SRL");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = (R2 < 32) ? (R1 >> R2) : (R1 << (R2-32));
				++PC;
				break;

			case 0b011:
				printf("LT");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = (R1 < R2) ? 1 : 0;
				++PC;
				break;

			case 0b100:
				printf("CP");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = R2;
				++PC;
				break;

			case 0b101:
				printf("CPI");
				if(i_flag) printf("i");
				printf("\n");

				if(i_flag){
					R1 = memory[A];
					R2 = memory[B];
					memory[R1] = R2;
				}else{
					R1 = memory[B];
					R2 = memory[R1];
					memory[A] = R2;
				}
				++PC;
				break;

			case 0b110:
				printf("BZJ");
				if(i_flag) printf("i");
				printf("\n");
				int PC_old = PC;
				if(i_flag){
					R1 = memory[A];
					R2 = B;
					PC = R1 + R2;
				}else{
					PC = (R2 == 0) ? R1 : (PC + 1);
				}

				halt = PC = PC_old;

				break;

			case 0b111:
				printf("MUL");
				if(i_flag) printf("i");
				printf("\n");

				memory[A] = R1 * R2;
				++PC;
				break;

			default:
				printf("what the fuck? how on earth did you get this error?\n");
				return 0;

		}

	}

	for (int i=0; i<RUN_LIMIT; ++i){
		printf("memloc %d= %u\n", i, memory[i]);
	}

} 
