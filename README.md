# gr-electrosense
An OOT module for electrosense sensor node. This implementation allows any user to connect to electrosense network with proper credentials and GNURadio installation.

## Dependencies

1. GNURadio
2. Apache Avro python bindings
3. MQTT python bindings


## Installation

### Basic installation

```
mkdir build ; cd build
cmake ../
make
sudo make install
```
### Enable GPU FFT block for RPI

Download the latest RPI gpu fft module from [here](http://www.aholme.co.uk/GPU_FFT/Main.htm "gpu_fft")

Extract the archive, then copy and  use **gpufft\_makefile** from extras directory to make a shared library

```
make clean
make -f gpufft_makefile
make 
sudo make install
```

Install gr-electrosense with GPU_FFT enabled 

```
mkdir build ; cd build
cmake ../ -DENABLE_GPUFFT=ON
make
sudo make install
```

## Available blocks
1. Discard samples 
	* Allows to discard samples from a continuous stream based on a variable change or tag
2. Sensor sink
	* Upstream connector block
3. MQTT client & Variable updater
	* Enables downstream variable control with optional authentication
4. Scanning module (embedded in flowgraph)
	* Supports sequential, random and similarity hopping patterns
5. RPI GPU FFT
	* Makes use of RPI gpu_fft module instead of FFTW

## Usage

### Sample examples
Check examples folder for detailed flowgraphs

### Downstream variable update
Setup mosquitto broker and perform a sample test locally 
```
mosquitto &
```
Analyse the channel 
```
mosquitto_sub -d -t electrosense
```
Run electrosense_mqtt_test.grc and try to change a variable 
```
mosquitto_pub -t electrosense -m "rfgain,10"
```

## ToDos

1. Detailed block output and speed testing
2. Detailed data validation testing with the backend
3. Embedded boards performance comparisons (RP1,2...)
