package com.socgame.campuswars_app.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.google.android.gms.maps.model.LatLng;
import com.google.firebase.auth.FirebaseAuth;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.BackendCom;
import com.socgame.campuswars_app.communication.FirebaseCom;
import com.socgame.campuswars_app.communication.HttpHeader;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/*
    Here we display info about the players team
    including a list of team members

    written by Jonas
 */
public class TeamFragment extends Fragment
{
    View fragmentView = null;

    private String color;
    private String teamName;
    private String[] members;

    public TeamFragment()
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
        Context ctx = this.getContext();

        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_team, container, false);
        this.fragmentView = view;

        ListView listView = view.findViewById(R.id.memberList);

        //Getting Button before Http Call so we can overwrite button color to team color
        Button rally = (Button) view.findViewById(R.id.raidButton);

        //Getting our Information from Backend and setting it in our GetResponseListener
        ctx = this.getContext();
        BackendCom bCom = BackendCom.getInstance(ctx);
        HttpHeader header = new HttpHeader(ctx);
        bCom.group(myGroupGet(rally), httpErrorListener(), header);


        rally.setOnClickListener(new View.OnClickListener()
        {
            public void onClick(View view)
            {
                //TODO: sent notification backend/firebase
                Toast.makeText(getActivity(), "You sent for your troops", Toast.LENGTH_LONG).show();
            }
        });

        return view;
    }

    public void setMembers(String[] names)
    {
        ListView listView = fragmentView.findViewById(R.id.memberList);

        //TODO: Create custom Array Adapter (not needed, unless we show more info)
        //ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_activated_1, array);
        ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(getContext(), R.layout.teammember, names);
        listView.setAdapter(itemsAdapter);
    }

    public void setTeamInfo(String name, int memberCount, int controlledHalls, String color)//TODO: maybe add team color?
    {
        //TODO EITHER FIX ISSUES WITH TRANSPARENCY OR USE COLOR WITHOUT TRANSPARENCY
        String desaturatedColor = color.replaceAll("#", "");
        desaturatedColor = "#80" + desaturatedColor;

        TextView nameText = fragmentView.findViewById(R.id.teamName);
        nameText.setText(name);
        nameText.setBackgroundTintList(ColorStateList.valueOf(Color.parseColor(desaturatedColor)));

        TextView memberText = fragmentView.findViewById(R.id.textCurrentMembers);
        memberText.setText(memberCount + " Members");

        TextView controlText = fragmentView.findViewById(R.id.textCurrentControll);
        controlText.setText(controlledHalls + "%");//WILL THIS BE ABSOLUTE OR PERCENT?
    }

    private Response.Listener<JSONObject> myGroupGet(Button button)
    {
        return new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    color = response.getString("colour");
                    teamName = response.getString("name");
                    JSONArray tMembers = response.getJSONArray("members");

                    members = new String[tMembers.length()];
                    for(int i = 0; i < tMembers.length(); i++){
                        members[i] = tMembers.getString(i);
                    }

                    setMembers(members);
                    setTeamInfo(teamName, members.length, 0, color);

                    //Setting Button Color to Team Color
                    button.setBackgroundTintList(ColorStateList.valueOf(Color.parseColor(color)));
                } catch (JSONException e) {
                    Log.d("My Group:", e.toString());
                }

            }
        };
    }

    private Response.ErrorListener httpErrorListener() {
        return new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //Error Handling
                Log.d("HTTP", "Error: " + error.getMessage());
            }
        };
    }

}