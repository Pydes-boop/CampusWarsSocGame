package com.socgame.campuswars_app.ui;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.graphics.Color;
import android.os.Bundle;
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
import com.socgame.campuswars_app.communication.GpsLocationManager;


public class MapsFragment extends Fragment
{

    private LatLng position;

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
        /**
         * Manipulates the map once available.
         * This callback is triggered when the map is ready to be used.
         * This is where we can add markers or lines, add listeners or move the camera.
         * In this case, we just add a marker near Sydney, Australia.
         * If Google Play services is not installed on the device, the user will be prompted to
         * install it inside the SupportMapFragment. This method will only be triggered once the
         * user has installed Google Play services and returned to the app.
         */

        @Override
        public void onMapReady(GoogleMap googleMap)
        {
            //Make it viusally fit our UI style
            googleMap.setMapStyle(MapStyleOptions.loadRawResourceStyle(getContext(), R.raw.mapsstyle_json));


            //Set marker at pos
            googleMap.addMarker(new MarkerOptions().position(position).title("You"));
            googleMap.moveCamera(CameraUpdateFactory.newLatLng(position));

            //Zoom in
            //if(position.latitude != 0 && position.longitude != 0)//dont zoom in on ocean debug
                googleMap.animateCamera( CameraUpdateFactory.zoomTo( 17.0f ) );



            //TODO: Get actual lecture halls
            // Add custom markers for our lecture halls
            double range = 0.005;
            for(int i = 0; i < 20; i++)
            {
                LatLng hall = new LatLng(position.latitude+(Math.random()*2-1)*range, position.longitude+(Math.random()*2-1)*range);

                Marker marker = googleMap.addMarker
                (
                        new MarkerOptions().position(hall).title("Lecture Hall " + i)
                        .icon(hexToHSV(/*"#" + Integer.toString(R.color.highlight)*/"#4275A8"))
                );
            }

            /*
            LatLng sydney = new LatLng(-34, 151);

            googleMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
            googleMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
            */
        }
    };


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

            //TODO: call this a lot, cause it does NOT auto update
            //Also this will crash if I call outside of this method
            //FML
            position = GpsLocationManager.getPosition(getActivity(), getContext());
        }
    }
}