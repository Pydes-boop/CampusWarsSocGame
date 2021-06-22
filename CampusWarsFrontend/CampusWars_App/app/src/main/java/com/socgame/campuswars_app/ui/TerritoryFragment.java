package com.socgame.campuswars_app.ui;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import com.socgame.campuswars_app.R;

public class TerritoryFragment extends Fragment //implements View.OnClickListener
{
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

        Button next = (Button) view.findViewById(R.id.challengeButton);
        next.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                Intent myIntent = new Intent(view.getContext(), QuizActivity.class);
                startActivityForResult(myIntent, 0);
            }
        });

        return view;
    }
}