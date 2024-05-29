import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def Watt2dBm(x):
	'''
	converts from units of watts to dBm
	'''
	return 10.*np.log10(x*1000.)
	
def dBm2Watt(x):
	'''
	converts from units of watts to dBm
	'''
	return 10**(x/10.) /1000.	

class plotting(object):
	'''
	some helper functions for plotting
	'''
	def plotall(self):
		real = self.z_data_raw.real
		imag = self.z_data_raw.imag
		real2 = self.z_data_sim.real
		imag2 = self.z_data_sim.imag
		plt.subplot(221)
		plt.plot(real,imag,label='rawdata')
		plt.plot(real2,imag2,label='fit')
		plt.xlabel('Re(S21)')
		plt.ylabel('Im(S21)')
		plt.legend()
		plt.subplot(222)
		plt.plot(self.f_data*1e-9,np.absolute(self.z_data_raw),label='rawdata')
		plt.plot(self.f_data*1e-9,np.absolute(self.z_data_sim),label='fit')
		plt.xlabel('f (GHz)')
		plt.ylabel('|S21|')
		plt.legend()
		plt.subplot(223)
		plt.plot(self.f_data*1e-9,np.angle(self.z_data_raw),label='rawdata')
		plt.plot(self.f_data*1e-9,np.angle(self.z_data_sim),label='fit')
		plt.xlabel('f (GHz)')
		plt.ylabel('arg(|S21|)')
		plt.legend()
		plt.show()
		
	def plotcombined(self):
		real = self.z_data_raw.real
		imag = self.z_data_raw.imag
		real2 = self.z_data_sim.real
		imag2 = self.z_data_sim.imag

		FIGURE_WIDTH_1COL = 3.404 
		FIGURE_WIDTH_2COL = 7.057
		FIGURE_HEIGHT_1COL_GR = FIGURE_WIDTH_1COL*2/(1 + np.sqrt(5))
		FIGURE_HEIGHT_2COL_GR = FIGURE_WIDTH_2COL*2/(1 + np.sqrt(5))

		fig = plt.figure(figsize=(FIGURE_WIDTH_1COL+1.3*FIGURE_HEIGHT_1COL_GR, FIGURE_WIDTH_1COL))
		gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])
        
		# Create subplots
		ax1 = fig.add_subplot(gs[:, 0])  # Span all rows in the first column
		ax2 = fig.add_subplot(gs[0, 1])  # First row, second column
		ax3 = fig.add_subplot(gs[1, 1], sharex=ax2)  # Second row, second column, sharing x-axis with ax2
		ax1.set_aspect('equal', adjustable='box')

		# Plot real and imaginary parts (the circle)
		ax1.scatter(real, imag, label='Data', s=0.5)
		ax1.plot(real2, imag2, color='darkorange', label='Fit')
		ax1.set_xlabel('Re[$S_{21}$]')
		ax1.set_ylabel('Im[$S_{21}$]')
		ax1.legend(loc='upper right')

		# Plot magnitude and phase
		ax2.scatter(self.f_data*1e-9,np.absolute(self.z_data_raw), label='Data', s=0.5)
		ax2.plot(self.f_data*1e-9,np.absolute(self.z_data_raw), color='darkorange', label='Fit')
		ax2.set_ylabel(r'$|S_{21}|$ [ ]')
		ax2.legend(loc='lower right')
		for ax in [ax2]:
			plt.setp(ax.get_xticklabels(), visible=False)	# set x-axis labels invisible

		ax3.scatter(self.f_data*1e-9,np.angle(self.z_data_raw), label='Data', s=0.5)
		ax3.plot(self.f_data*1e-9,np.angle(self.z_data_raw), color='darkorange', label='Fit')
		ax3.set_xlabel('Frequency [GHz]')
		ax3.set_ylabel(r'$arg(S_{21})$ [deg]')
		ax3.set_xlim([6.45, 6.75])
		ax3.legend(loc='lower right')
		plt.show()


	def plotcalibrateddata(self):
		real = self.z_data.real
		imag = self.z_data.imag
		plt.subplot(221)
		plt.plot(real,imag,label='rawdata')
		plt.xlabel('Re(S21)')
		plt.ylabel('Im(S21)')
		plt.legend()
		plt.subplot(222)
		plt.plot(self.f_data*1e-9,np.absolute(self.z_data),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('|S21|')
		plt.legend()
		plt.subplot(223)
		plt.plot(self.f_data*1e-9,np.angle(self.z_data),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('arg(|S21|)')
		plt.legend()
		plt.show()
		
	def plotrawdata(self):
		real = self.z_data_raw.real
		imag = self.z_data_raw.imag
		plt.subplot(221)
		plt.plot(real,imag,label='rawdata')
		plt.xlabel('Re(S21)')
		plt.ylabel('Im(S21)')
		plt.legend()
		plt.subplot(222)
		plt.plot(self.f_data*1e-9,np.absolute(self.z_data_raw),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('|S21|')
		plt.legend()
		plt.subplot(223)
		plt.plot(self.f_data*1e-9,np.angle(self.z_data_raw),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('arg(|S21|)')
		plt.legend()
		plt.show()

class save_load(object):
	'''
	procedures for loading and saving data used by other classes
	'''
	def _ConvToCompl(self,x,y,dtype):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		if dtype=='realimag':
			return x+1j*y
		elif dtype=='linmagphaserad':
			return x*np.exp(1j*y)
		elif dtype=='dBmagphaserad':
			return 10**(x/20.)*np.exp(1j*y)
		elif dtype=='linmagphasedeg':
			return x*np.exp(1j*y/180.*np.pi)
		elif dtype=='dBmagphasedeg':
			return 10**(x/20.)*np.exp(1j*y/180.*np.pi)	 
		else: warnings.warn("Undefined input type! Use 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg' or 'linmagphasedeg'.", SyntaxWarning)
	
	def add_data(self,f_data,z_data):
		self.f_data = np.array(f_data)
		self.z_data_raw = np.array(z_data)
		
	def cut_data(self,f1,f2):
		def findpos(f_data,val):
			pos = 0
			for i in range(len(f_data)):
				if f_data[i]<val: pos=i
			return pos
		pos1 = findpos(self.f_data,f1)
		pos2 = findpos(self.f_data,f2)
		self.f_data = self.f_data[pos1:pos2]
		self.z_data_raw = self.z_data_raw[pos1:pos2]
		
	def add_fromtxt(self,fname,dtype,header_rows,usecols=(0,1,2),fdata_unit=1.,delimiter=None):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		data = np.loadtxt(fname,usecols=usecols,skiprows=header_rows,delimiter=delimiter)
		self.f_data = data[:,0]*fdata_unit
		self.z_data_raw = self._ConvToCompl(data[:,1],data[:,2],dtype=dtype)
		
	def add_fromhdf():
		pass
	
	def add_froms2p(self,fname,y1_col,y2_col,dtype,fdata_unit=1.,delimiter=None):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		if dtype == 'dBmagphasedeg' or dtype == 'linmagphasedeg':
			phase_conversion = 1./180.*np.pi
		else: 
			phase_conversion = 1.
		f = open(fname)
		lines = f.readlines()
		f.close()
		z_data_raw = []
		f_data = []
		if dtype=='realimag':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!")) :
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					z_data_raw.append(complex(float(lineinfo[y1_col]),float(lineinfo[y2_col])))
		elif dtype=='linmagphaserad' or dtype=='linmagphasedeg':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!") and (line[0]!="M") and (line[0]!="P")):
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					z_data_raw.append(float(lineinfo[y1_col])*np.exp( complex(0.,phase_conversion*float(lineinfo[y2_col]))))
		elif dtype=='dBmagphaserad' or dtype=='dBmagphasedeg':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!") and (line[0]!="M") and (line[0]!="P")):
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					linamp = 10**(float(lineinfo[y1_col])/20.)
					z_data_raw.append(linamp*np.exp( complex(0.,phase_conversion*float(lineinfo[y2_col]))))
		else:
			warnings.warn("Undefined input type! Use 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg' or 'linmagphasedeg'.", SyntaxWarning)
		self.f_data = np.array(f_data)
		self.z_data_raw = np.array(z_data_raw)
		
	def save_fitresults(self,fname):
		pass
	


