# From: 
#  https://github.com/nikizadehgfdl/grid_generation/blob/dev/jupynotebooks/regional_grid_spherical.ipynb

#General imports and definitions
import cartopy
import numpy as np
import matplotlib.pyplot as plt

# For use with python notebooks
#%matplotlib inline

class gridUtils:

    def __init__(self):
        #Constants
        self.PI_180 = np.pi/180.
        self._default_Re = 6.378e6
    
    def mesh_plot(self, lon, lat, lon0=0., lat0=90.):
        """Plot a given mesh with a perspective centered at (lon0,lat0)"""
        plt.figure(figsize=(8,8))
        ax = plt.subplot(111, projection=cartopy.crs.NearsidePerspective(central_longitude=lon0, central_latitude=lat0))
        ax.set_global()
        ax.stock_img()
        ax.coastlines()
        ax.gridlines()
        (nj,ni) = lon.shape 
        # plotting verticies
        for i in range(0,ni+1,2):
            ax.plot(lon[:,i], lat[:,i], 'k', transform=cartopy.crs.Geodetic())
        for j in range(0,nj+1,2):
            ax.plot(lon[j,:], lat[j,:], 'k', transform=cartopy.crs.Geodetic())
    
    def rotate_x(self,x,y,z,theta):
        """Rotate vector (x,y,z) by angle theta around x axis."""
        """Returns the rotated components."""
        cost = np.cos(theta)
        sint = np.sin(theta)
        yp   = y*cost - z*sint
        zp   = y*sint + z*cost
        return x,yp,zp
    
    def rotate_y(self,x,y,z,theta):
        """Rotate vector (x,y,z) by angle theta around y axis."""
        """Returns the rotated components."""
        cost = np.cos(theta)
        sint = np.sin(theta)
        zp   = z*cost - x*sint
        xp   = z*sint + x*cost
        return xp,y,zp
    
    def rotate_z(self,x,y,z,theta):
        """Rotate vector (x,y,z) by angle theta around z axis."""
        """Returns the rotated components."""
        cost = np.cos(theta)
        sint = np.sin(theta)
        xp   = x*cost - y*sint
        yp   = x*sint + y*cost
        return xp,yp,z
    
    
    def cart2pol(self,x,y,z):
        """Transform a point on globe from Cartesian (x,y,z) to polar coordinates."""
        """Returns the polar coordinates"""
        lam=np.arctan2(y,x)/self.PI_180
        phi=np.arctan(z/np.sqrt(x**2+y**2))/self.PI_180
        return lam,phi
    
    def pol2cart(self,lam,phi):
        """Transform a point on globe from Polar (lam,phi) to Cartesian coordinates."""
        """Returns the Cartesian coordinates"""
        lam=lam*self.PI_180
        phi=phi*self.PI_180
        x=np.cos(phi)*np.cos(lam)
        y=np.cos(phi)*np.sin(lam)
        z=np.sin(phi)
        return x,y,z
        
    def rotate_z_mesh(self,lam,phi,theta):
        """Rotate the whole mesh on globe by angle theta around z axis (globe polar axis)."""
        """Returns the rotated mesh."""
        #Bring the angle to be in [-pi,pi] so that atan2 would work
        lam       = np.where(lam>180,lam-360,lam)
        #Change to Cartesian coord
        x,y,z     = self.pol2cart(lam,phi)
        #Rotate
        xp,yp,zp  = self.rotate_z(x,y,z,theta)
        #Change back to polar coords using atan2, in [-pi,pi]
        lamp,phip = self.cart2pol(xp,yp,zp)
        #Bring the angle back to be in [0,2*pi]
        lamp      = np.where(lamp<0,lamp+360,lamp)
        return lamp,phip
    
    def rotate_x_mesh(self,lam,phi,theta):
        """Rotate the whole mesh on globe by angle theta around x axis (passing through equator and prime meridian.)."""
        """Returns the rotated mesh."""
        #Bring the angle to be in [-pi,pi] so that atan2 would work
        lam       = np.where(lam>180,lam-360,lam)
        #Change to Cartesian coord
        x,y,z     = self.pol2cart(lam,phi)
        #Rotate
        xp,yp,zp  = self.rotate_x(x,y,z,theta)
        #Change back to polar coords using atan2, in [-pi,pi]
        lamp,phip = self.cart2pol(xp,yp,zp)
        #Bring the angle back to be in [0,2*pi]
        lamp      = np.where(lamp<0,lamp+360,lamp)
        return lamp,phip
    
    def rotate_y_mesh(self,lam,phi,theta):
        """Rotate the whole mesh on globe by angle theta around y axis (passing through equator and prime meridian+90.)."""
        """Returns the rotated mesh."""
        #Bring the angle to be in [-pi,pi] so that atan2 would work
        lam       = np.where(lam>180,lam-360,lam)
        #Change to Cartesian coord
        x,y,z     = self.pol2cart(lam,phi)
        #Rotate
        xp,yp,zp  = self.rotate_y(x,y,z,theta)
        #Change back to polar coords using atan2, in [-pi,pi]
        lamp,phip = self.cart2pol(xp,yp,zp)
        #Bring the angle back to be in [0,2*pi]
        lamp      = np.where(lamp<0,lamp+360,lamp)
        return lamp,phip
    
    def generate_latlon_mesh_centered(self,lni,lnj,llon0,llen_lon,llat0,llen_lat, ensure_nj_even=True):
        """Generate a regular lat-lon grid"""
        print('Generating regular lat-lon grid between ceneterd at ', llon0, llat0)
        llonSP = llon0 - llen_lon/2 + np.arange(lni+1) * llen_lon/float(lni)
        llatSP = llat0 - llen_lat/2 + np.arange(lnj+1) * llen_lat/float(lnj)
        if(llatSP.shape[0]%2 == 0 and ensure_nj_even):
            print("   The number of j's is not even. Fixing this by cutting one row at south.")
            llatSP = np.delete(llatSP,0,0)
        llamSP = np.tile(llonSP,(llatSP.shape[0],1))
        lphiSP = np.tile(llatSP.reshape((llatSP.shape[0],1)),(1,llonSP.shape[0]))
        print('   generated regular lat-lon grid between latitudes ', lphiSP[0,0],lphiSP[-1,0])
        print('   number of js=',lphiSP.shape[0])
    #    h_i_inv=llen_lon*self.PI_180*np.cos(lphiSP*self.PI_180)/lni
    #    h_j_inv=llen_lat*self.PI_180*np.ones(lphiSP.shape)/lnj
    #    delsin_j = np.roll(np.sin(lphiSP*self.PI_180),shift=-1,axis=0) - np.sin(lphiSP*self.PI_180)
    #    dx_h=h_i_inv[:,:-1]*self._default_Re
    #    dy_h=h_j_inv[:-1,:]*self._default_Re
    #    area=delsin_j[:-1,:-1]*self._default_Re*self._default_Re*llen_lon*self.self.PI_180/lni
        return llamSP,lphiSP
    
    
    def generate_regional_spherical(self,lon0,lon_span,lat0,lat_span,tilt,refine):
        """Generate a regional grid centered at (lon0,lat0) with spans of (lon_span,lat_span) and tilted by angle tilt"""
        Ni = int(lon_span*refine)
        Nj = int(lat_span*refine)
       
        #Generate a mesh at equator centered at (lon0, 0)
        lam_,phi_ = self.generate_latlon_mesh_centered(Ni,Nj,lon0,lon_span,0.0,lat_span)
        lam_,phi_ = self.rotate_z_mesh(lam_,phi_, (90.-lon0)*self.PI_180)  #rotate around z to bring it centered at y axis
        lam_,phi_ = self.rotate_y_mesh(lam_,phi_,tilt*self.PI_180)         #rotate around y axis to tilt it as desired
        lam_,phi_ = self.rotate_x_mesh(lam_,phi_,lat0*self.PI_180)         #rotate around x to bring it centered at (lon0,lat0)
        lam_,phi_ = self.rotate_z_mesh(lam_,phi_,-(90.-lon0)*self.PI_180)  #rotate around z to bring it back 
        return lam_,phi_
