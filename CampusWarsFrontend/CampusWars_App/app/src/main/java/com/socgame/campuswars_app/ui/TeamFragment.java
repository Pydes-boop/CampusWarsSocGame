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

        String[] array =
        {
            "Dummy Name 1",
            "Dummy Name 2",
            "Dummy Name 3",
        };

        //TODO: Create custom Array Adapter
        ArrayAdapter<String> itemsAdapter = new ArrayAdapter<String>(getContext(), android.R.layout.simple_list_item_activated_1, array);
        listView.setAdapter(itemsAdapter);

        return view;
    }
}