package com.socgame.campuswars_app.Sensor;

import android.app.Activity;

import com.google.android.gms.maps.model.LatLng;

/*
    implement this, call the register method and override OnLocationUpdate to recieve the GPS coordinates
    (GPS Listener / Observable will be automatically created)

    written by Jonas
*/
public interface GpsObserver
{
    public void OnLocationUpdate(LatLng loc);

    public default void register(Activity activity)
    {
        GpsListener instance = GpsListener.getInstance(activity);

        if(instance != null)
            instance.register(this);
        //else TODO: Log erronious state
    }

    public default void unregister(Activity activity)
    {
        GpsListener instance = GpsListener.getInstance(activity);

        if(instance != null)
            instance.unregister(this);
        //else TODO: Log erronious state
    }
}
