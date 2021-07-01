package com.socgame.campuswars_app.ui;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.service.autofill.FieldClassification;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.google.android.gms.maps.model.LatLng;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.Sensor.GpsObserver;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.HttpHeader;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/*

*/
public class TerritoryFragment extends Fragment  implements GpsObserver //implements View.OnClickListener
{
    View fragmentView = null;
    private Context ctx;
    private BackendCom bCom;
    private int lectureId;
    private String lectureHall = "nothing";
    private LatLng lectureLoc = null;

    //TODO: create an update method which calls the server

    public TerritoryFragment()
    {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_territory, container, false);
        this.fragmentView = view;

        ctx = this.getContext();
        bCom = BackendCom.getInstance(ctx);

        Button challenge = (Button) view.findViewById(R.id.challengeButton);
        challenge.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                if(lectureHall.equals("nothing")){
                    Toast.makeText(getActivity(), "You need to enter a lecture hall to challenge people", Toast.LENGTH_LONG).show();
                } else {
                    Intent myIntent = new Intent(view.getContext(), MatchMakingActivity.class);
                    //We use bundles to give parameters to our QuizActivity
                    Bundle b = new Bundle();
                    b.putDouble("latitude", lectureLoc.latitude); //Question
                    b.putDouble("longitude", lectureLoc.longitude); //Question
                    b.putString("roomName", lectureHall); //Challenger name
                    b.putInt("lid", lectureId); //Challenger name
                    myIntent.putExtras(b);
                    startActivityForResult(myIntent, 0);
                }
            }
        });


        Button rally = (Button) view.findViewById(R.id.raidButton);
        rally.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view)
            {
                //TODO: sent notification backend/firebase
                Toast.makeText(getActivity(), "You sent for your troops", Toast.LENGTH_LONG).show();
            }
        });


        registerForContextMenu(getView());

        return view;
    }

    public void setHallInfo(String name, String owner, String lecture, LatLng loc)//TODO: maybe add color?
    {
        lectureLoc = loc;

        TextView nameText = fragmentView.findViewById(R.id.lectureHall);
        nameText.setText(name);
        //nameText.setColor(color);

        TextView ownerText = fragmentView.findViewById(R.id.textCurrentOwner);
        ownerText.setText(owner);

        TextView lectureText = fragmentView.findViewById(R.id.textCurrentLecture);
        lectureText.setText(lecture);
    }

    private Response.Listener<JSONObject> roomfinderPostListener(double latitude, double longitude)
    {
        return new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    JSONObject occupancy = response.getJSONObject("occupancy");
                    String occupier = response.getString("occupier");

                    int lid = response.getInt("lid");
                    lectureId = lid;
                    double multiplier = response.getDouble("multiplier");

                    String name = response.getString("room_name");

                    setHallInfo(name, occupier, "No Lecture currently", new LatLng(latitude, longitude));

                } catch (Exception e) {
                    Log.d("Error in Roomfinder Call", e.toString());
                }
            }
        };
    }

    private Response.ErrorListener httpErrorListener() {
        return new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                lectureHall = "nothing";
                //Error Handling
                Log.d("HTTP", "Error: " + error.getMessage());
            }
        };
    }

    @Override
    public void OnLocationUpdate(LatLng loc)
    {
        HttpHeader head = new HttpHeader(ctx);
        head.buildRoomFinderHeader(loc.latitude, loc.longitude);
        bCom.roomDetectionPost(roomfinderPostListener(loc.latitude, loc.longitude), httpErrorListener(), head);

        //maybe safe last location?
        //maybe do some distance / time checks
        //TODO ROOMFINDER CALL HERE?
    }
}