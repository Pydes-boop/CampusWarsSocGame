package com.socgame.campuswars_app.ui;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptor;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MapStyleOptions;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.Sensor.GpsObserver;

/**
   * Displays the world map
   * Uses custom design
   * Displays current position
   * Displays lecture halls
   *
   * written by Jonas
*/
public class MapsFragment extends Fragment implements GpsObserver
{
    private LatLng position = new LatLng(48.2650,11.6716);//Using campus as default/fallback position;
    private GoogleMap map;
    private Marker localPos;//TODO: maybe google maps has an integrated way to do that?

    //Thanks StackOverflow
    //https://stackoverflow.com/questions/19076124/android-map-marker-color
    private static BitmapDescriptor hexToHSV(String hexColor)
    {
        float[] hsv = new float[3];
        Color.colorToHSV(Color.parseColor(hexColor), hsv);
        return BitmapDescriptorFactory.defaultMarker(hsv[0]);
    }

    private OnMapReadyCallback callback = new OnMapReadyCallback()
    {
        @Override
        public void onMapReady(GoogleMap googleMap)
        {
            map = googleMap;


            //Make it viusally fit our UI style
            googleMap.setMapStyle(MapStyleOptions.loadRawResourceStyle(getContext(), R.raw.mapsstyle_json));


            //same code in gps update

            //Set marker at pos
            localPos =  googleMap.addMarker(new MarkerOptions().position(position).title("You"));

            //Set cam to pos
            googleMap.moveCamera(CameraUpdateFactory.newLatLng(position));
            
            //Zoom in
            googleMap.animateCamera( CameraUpdateFactory.zoomTo( 17.0f ) );

            /*
            //NICE TO HAVE
            //DRAW BORDERS
            //https://stackoverflow.com/questions/45803711/how-to-draw-a-polygon-like-google-map-in-android-app
            /*
            Polygon polygon = googleMap.addPolygon(new PolygonOptions()
                    .add
                    (
                        new LatLng(position.latitude+(Math.random()*2-1)*range/3, position.longitude+(Math.random()*2-1)*range),
                        new LatLng(position.latitude+(Math.random()*2-1)*range/3, position.longitude+(Math.random()*2-1)*range),
                        new LatLng(position.latitude+(Math.random()*2-1)*range/3, position.longitude+(Math.random()*2-1)*range)
                    )
                    .strokeColor(Color.BLUE)
                    .fillColor(Color.CYAN));
            */
        }
    };


    //Adding proper comments, cause Daniel will have to call this

    /**
     * Add a marker of a lecture hall to the map.
     * Wrapper of identical method which uses the LatLng class for gps pos
     *
     *
     * @param lat latitude
     * @param lon longitude
     * @param color marker color as hex example: "#4275A8"
     * @param name name of lecture hall
     * @param lecture current lecture title, alternatively any sub-headline
     * @return reference of the Marker. Call Marker.remove() to delete lecture hall
     */
    public Marker addLectureHall(double lat, double lon, String color, String name, String lecture)
    {
        return addLectureHall(new LatLng(lat, lon), color, name, lecture);
    }

    /**
     * Add a marker of a lecture hall to the map
     *
     * @param pos gps location
     * @param color marker color as hex example: "#4275A8"
     * @param name name of lecture hall
     * @param lecture current lecture title, alternatively any sub-headline
     * @return reference of the Marker. Call Marker.remove() to delete lecture hall
     */
    public Marker addLectureHall(LatLng pos, String color, String name, String lecture)
    {
        //TODO: maybe safe locally for further analysis?


        String fallbackColor = "#4275A8";

        BitmapDescriptor markerIcon;
        //BitmapDescriptor towerIcon = BitmapDescriptorFactory.fromResource(R.drawable.ic_territory);

        try //Check color viability
        {
            markerIcon = hexToHSV(color);
        }
        catch (Exception e)
        {
            Log.e("GPS", "Could not parse color " + color);
            markerIcon = hexToHSV(fallbackColor);
        }


        Marker marker = map.addMarker
                (
                        new MarkerOptions().position(pos).title(name)
                                .icon(markerIcon)
                                .snippet(lecture)
                );

        return  marker;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_maps, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState)
    {
        super.onViewCreated(view, savedInstanceState);
        SupportMapFragment mapFragment = (SupportMapFragment) getChildFragmentManager().findFragmentById(R.id.map);

        if (mapFragment != null)
        {
            mapFragment.getMapAsync(callback);

            mapFragment.setMenuVisibility(false);
            mapFragment.setHasOptionsMenu(false);

            register(getActivity());//Also creates instance of gps listener if needed and autoupdates itself
        }

    }

    @Override
    public void OnLocationUpdate(LatLng loc)
    {
        if(loc == null)
        {
            Log.e("GPS", this + " recieved null location");
        }

        position = loc;

        Log.d("GPS", this + " location updated to " + loc.latitude + ", " + loc.longitude);

        if(map != null)
        {

            //TODO: smooth camera
            //TODO: dont always move camera


            //move camera
            map.moveCamera(CameraUpdateFactory.newLatLng(position));
            //Zoom in
            map.animateCamera( CameraUpdateFactory.zoomTo( 17.0f ) );


            if(localPos != null)
            {
                localPos.remove();
                localPos =  map.addMarker(new MarkerOptions().position(position).title("You"));
            }
        }
    }
}
