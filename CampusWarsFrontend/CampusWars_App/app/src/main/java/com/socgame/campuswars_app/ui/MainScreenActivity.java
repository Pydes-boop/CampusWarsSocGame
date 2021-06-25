package com.socgame.campuswars_app.ui;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

import com.google.android.gms.maps.GoogleMapOptions;
import com.google.android.material.tabs.TabLayout;
import com.socgame.campuswars_app.custom.CustomViewPager;
import com.socgame.campuswars_app.R;

/*
    Displays the heart of our game
    Three tabs (lecture hall, map, team)

    uses custom ViewPager

    written by both Daniel and Jonas
*/
public class MainScreenActivity extends AppCompatActivity
{
    private TabLayout tabLayout;
    private SectionsPagerAdapter mSectionsPagerAdapter;
    private CustomViewPager mViewPager;

    //Icons in Tab Bar
    private int[] tabIcons = {
            R.drawable.ic_territory,
            R.drawable.ic_map_icon,
            R.drawable.ic_group_icon
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_screen);


        //Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        //setSupportActionBar(toolbar);
        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());
        // Set up the ViewPager with the sections adapter.
        mViewPager = findViewById(R.id.view_pager);
        //Disable Swiping
        mViewPager.setPagingEnabled(false);//Swiping
        mViewPager.setAdapter(mSectionsPagerAdapter);


        TabLayout tabLayout = findViewById(R.id.tab_layout);
        tabLayout.setupWithViewPager(mViewPager);

        //Adding Icons to Tabs
        for(int i = 0; i < 3; i++){
            tabLayout.getTabAt(i).setIcon(tabIcons[i]);
        }
    }

    public class SectionsPagerAdapter extends FragmentPagerAdapter {
        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }
        @Override
        public Fragment getItem(int position) {
            Fragment fragment = null;
            switch (position) {
                case 0:
                    fragment = new TerritoryFragment();//new QuizFragment().newInstance("Hello", "Ciao");
                    break;
                case 1:
                    fragment = new MapsFragment();//.newInstance(new GoogleMapOptions().mapId("e28f2141bdd678c1"));
                    break;
                case 2:
                    fragment = new TeamFragment();//new TerritoryFragment();
                    break;
            }
            return fragment;
        }
        @Override
        public int getCount() //Number of possible Fragments
        {
            // Show 3 total pages.
            return 3;
        }
        @Override
        public CharSequence getPageTitle(int position) //Page Title
        {
            //No Text, only Picture >.<
            /*switch (position) {
                case 0:
                    return "Quiz";
                case 1:
                    return "Maps";
                case 2:
                    return "Territory";
            }*/
            return null;
        }
    }
}
