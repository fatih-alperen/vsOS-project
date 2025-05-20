#include <stdio.h>
#include <stdint.h>


int main(int argc, char* argv[]){

	size_t MEM_SIZE = 512*1024;
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
	while(PC < 10){
		uint32_t instruction = memory[PC];
		uint32_t opcode = (instruction >> 29) & 0b111;
		uint32_t i_flag = (instruction >> 28) & 1;
		uint32_t R1 = (instruction >> 14) & 0x3FFF;
		uint32_t R2 = (instruction) & 0x3FFF;
		printf("PC: %d, instruction: %d\n", PC, instruction);

		switch(opcode){
		
			case 0b000:
				printf("ADD");
				R1 = instruction >> 27
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b001:
				printf("NAND");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b010:
				printf("SRL");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b011:
				printf("LT");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b100:
				printf("CP");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b101:
				printf("CPI");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b110:
				printf("BZJ");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			case 0b111:
				printf("MUL");
				if(i_flag) printf("i");
				printf("\n");
				++PC;
				break;
			default:
				return 0;

		}

	}

} 
