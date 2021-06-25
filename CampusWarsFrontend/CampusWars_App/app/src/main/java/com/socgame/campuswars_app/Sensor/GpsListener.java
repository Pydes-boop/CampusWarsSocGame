package com.socgame.campuswars_app.Sensor;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;

import com.google.android.gms.maps.model.LatLng;

import java.util.LinkedList;
import java.util.List;


/*
    Register to this (Singleton) observable to get your location (as Lat Long)
    Use get Instance, never call a constructor yourself!!!!

    I absolutly hate everything about this. Is cost me blood sweat and tears - mostly tears

    written by Jonas
 */
public class GpsListener implements LocationListener
{
    //Singleton
    private static GpsListener instance;

    //DO NOT USE THE CONSTRUCTOR!!
    private GpsListener(Activity activity)
    {
        if (instance == null)
        {
            instance = this;

            Log.d("GPS", "Initialized GPS Listener");

            /*
            //Activity needed to create a locationmanager
           class DummyActivity extends Activity
           {
               @Override
               protected void onCreate(@Nullable Bundle savedInstanceState)
               {
                   super.onCreate(savedInstanceState);
                   //Dont show anything
                   //no intent
                   //no starting
               }
           }
           DummyActivity activity = new DummyActivity();
           Bundle savedInstance = Bundle.EMPTY;
           activity.onCreate(savedInstance);
            */

           LocationManager lm = (LocationManager) activity.getSystemService(activity.LOCATION_SERVICE);

            //Permission checks
           if
           (
               ActivityCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED
           )
           {
               activity.requestPermissions
                       (
                                new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION},
                                42069
                       );
               //return;
           }


            try
            {
                //startlocation
                String provider = LocationManager.GPS_PROVIDER;
                Location lastLoc = lm.getLastKnownLocation(provider);

                //Force location update
                lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 1, this);
                lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 1000, 1, this);
            }
            catch (Exception e) {Log.e("GPS", "Could not start GPS: " + e);}
        }
    }

    //USE THIS TO ACCESS THE CLASS
    public static GpsListener getInstance(Activity activity)//TODO: I REALLY HATE HAVING TO GIVE AN ACTIVITY HERE! I WANT TO BE ABLE TO GET GPS FROM NORMAL JAVA
    {
        if(instance == null)
            instance = new GpsListener(activity);

        return instance;
    }

    //Observer Stuff
    private List<GpsObserver> observers = new LinkedList<GpsObserver>();

    //returns false if called on the wrong object instance
    public boolean register(GpsObserver observer)
    {
        if(this != instance)
            return false;


        //If I am can, try to explicitly get permission
        Activity activity = null;
        Fragment fragment = null;

        try
        {
            activity = (Activity) observer;
        }
        catch (Exception e) {}

        try
        {
            fragment = (Fragment) observer;
        }
        catch (Exception e) {}

        if(activity == null && fragment != null)
            activity = fragment.getActivity();
        if(activity != null)
        {
            activity.requestPermissions
            (
                new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION},
                42069
            );
        }

        //Register
        observers.add(observer);
        observer.OnLocationUpdate(location);//Initialize

        return true;
    }

    //returns false if called on the wrong object instance
    //it does return true however if the observer wasnt registered anyway
    public boolean unregister(GpsObserver observer)
    {
        if(this != instance)
            return false;

        observers.remove(observer);

        return true;
    }

    //notify all the observers of my new location
    private void update()
    {
        for (GpsObserver observer : observers)
        {
            observer.OnLocationUpdate(location);
        }
    }


    //Actual location logic
    private LatLng location = new LatLng(48.2650,11.6716);//Using campus as default/fallback position


    @Override
    public void onLocationChanged(@NonNull Location location)
    {
        //TODO: DO CHECKS
        LatLng loc = locToLatLng(location);
        this.location = loc;

        Log.d("GPS", "Location changed to " + location.getLatitude() + ", " + location.getLongitude());

        update();
    }

    //NOT SUPPORTED IN THIS ANDROID VERSION
    /*
    @Override
    public void onLocationChanged(@NonNull List<Location> locations)
    {
        double lat = 0;
        double lng = 0;

        for(Location loc : locations)
        {
            //TODO: factor in accuracy
            lat += loc.getLatitude();
            lng += loc.getLongitude();
        }

        LatLng loc = new LatLng(lat, lng);
        this.location = loc;

        Log.d("GPS", "Location changed to " + lat + ", " + lng);

        update();
    }
     */

    @Override
    public void onProviderDisabled(@NonNull String provider)
    {
        Log.d("GPS", "Could not use provider " + provider);
    }

    private static LatLng locToLatLng(Location loc)
    {
        return new LatLng(loc.getLatitude(), loc.getLongitude());
    }
}
