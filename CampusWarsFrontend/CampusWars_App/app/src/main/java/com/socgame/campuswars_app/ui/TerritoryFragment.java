package com.socgame.campuswars_app.ui;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Response;
import com.google.android.gms.maps.model.LatLng;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.Sensor.GpsObserver;

import org.json.JSONArray;

/*

*/
public class TerritoryFragment extends Fragment  implements GpsObserver //implements View.OnClickListener
{
    View fragmentView = null;

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

        Button challenge = (Button) view.findViewById(R.id.challengeButton);
        challenge.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), QuizActivity.class);
                //We use bundles to give parameters to our QuizActivity
                Bundle b = new Bundle();
                b.putString("question", "Which one of these Sports typically requires a social Context?"); //Question
                b.putStringArray("answers", new String[]{"Swimming", "Gaming", "Basketball", "Running"}); //Answer Options
                b.putInt("correctAnswer", 3); //Correct Answer
                b.putString("challenger", "Georg Groh"); //Challenger name
                myIntent.putExtras(b);
                startActivityForResult(myIntent, 0);
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

    public void setHallInfo(String name, String owner, String lecture)//TODO: maybe add color?
    {
        TextView nameText = fragmentView.findViewById(R.id.lectureHall);
        nameText.setText(name);
        //nameText.setColor(color);

        TextView ownerText = fragmentView.findViewById(R.id.textCurrentOwner);
        ownerText.setText(owner);

        TextView lectureText = fragmentView.findViewById(R.id.textCurrentLecture);
        lectureText.setText(lecture);
    }

    private Response.Listener<JSONArray> roomfinderPostListener()
    {
        return new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {

                //TODO: get actual info from server
                setHallInfo("Current Lecture Hall", "Owning Team Name", "Current Lecture");
            }
        };
    }

    @Override
    public void OnLocationUpdate(LatLng loc)
    {
        //maybe safe last location?
        //maybe do some distance / time checks
        //TODO ROOMFINDER CALL HERE?
    }
}