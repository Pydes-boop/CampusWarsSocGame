package com.socgame.campuswars_app.ui;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import com.google.firebase.auth.FirebaseAuth;
import com.socgame.campuswars_app.R;
import com.socgame.campuswars_app.communication.FirebaseCom;

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

        Button logout = (Button) view.findViewById(R.id.logoutButton);
        FirebaseCom fCom = FirebaseCom.getInstance(ctx);

        //TODO: get correct info from server
        //only possible when the calls exist
        String[] array =
        {
            "Dummy Name 1",
            "Dummy Name 2",
            "Dummy Name 3",
            "Dummy Name 4",
            "Dummy Name 5",
            "Dummy Name 6",
            "Dummy Name 7",
            "Dummy Name 8",
            "Dummy Name 9",
            "Dummy Name 10",
        };

        setMembers(array);
        setTeamInfo("Your Team Name", 5, 10);

        //Logout Button
        logout.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                fCom.getMAuth().signOut();
                SharedPreferences settings = ctx.getSharedPreferences("userdata", 0);
                SharedPreferences.Editor editor = settings.edit();
                editor.putBoolean("loggedIn", false);
                editor.apply();

                Intent myIntent = new Intent(view.getContext(), LoginActivity.class);
                startActivityForResult(myIntent, 0);
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

    public void setTeamInfo(String name, int memberCount, int controlledHalls)//TODO: maybe add team color?
    {
        TextView nameText = fragmentView.findViewById(R.id.teamName);
        nameText.setText(name);
        //nameText.setTextColor();

        TextView memberText = fragmentView.findViewById(R.id.textCurrentMembers);
        memberText.setText(memberCount + " Members");

        TextView controlText = fragmentView.findViewById(R.id.textCurrentControll);
        controlText.setText(controlledHalls + "%");//WILL THIS BE ABSOLUTE OR PERCENT?
    }
}