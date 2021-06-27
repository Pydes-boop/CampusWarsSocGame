package com.socgame.campuswars_app.ui;

import android.content.Context;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.socgame.campuswars_app.R;

import java.util.ArrayList;
import java.util.List;

/*
    Here we display info about the players team
    including a list of team members

    written by Jonas
 */
public class TeamFragment extends Fragment
{
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
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_team, container, false);
        ListView listView = view.findViewById(R.id.memberList);

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

        //TODO: Create custom Array Adapter
        //ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_activated_1, array);
        ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(getContext(), R.layout.teammember, array);
        listView.setAdapter(itemsAdapter);

        return view;
    }
}