# -*- coding: utf-8 -*-

import datetime
import ttcal
from dk import utidy
from django import template


expected = u'''
<table class="month">
    <thead>
        <tr>
            <th class="month-name month-navigation" colspan="7" id="m20125">
                <div class="month-navigation-prev">
                    <a href="../m20124/">
                        <img src="//static.datakortet.no/ikn/afr/afr-frev-white.gif">
                    </a>
                </div>
                <div class="month-navigation-next">
                    <a href="../m20126/">
                        <img src="//static.datakortet.no/ikn/afr/afr-ffwd-white.gif">
                    </a>
                </div>
                Mai, 2012
            </th>
        </tr>
        <tr class="day-name">
            <th>
                Mandag
            </th>
            <th>
                Tirsdag
            </th>
            <th>
                Onsdag
            </th>
            <th>
                Torsdag
            </th>
            <th>
                Fredag
            </th>
            <th>
                Lørdag
            </th>
            <th>
                Søndag
            </th>
        </tr>
    </thead>
    <tbody>
        <tr class="w201218">
            <td class="class" day="30" id="d2012043005" month="4" week="18" year="2012">
                <div class="content">
                    &nbsp;
                </div>
            </td>
            <td class="dc" day="1" id="d2012050105" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        1
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="2" id="d2012050205" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        2
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="3" id="d2012050305" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        3
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="4" id="d2012050405" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        4
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="5" id="d2012050505" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        5
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="6" id="d2012050605" month="5" week="18" year="2012">
                <div class="content">
                    <div class="daynum">
                        6
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
        </tr>
        <tr class="w201219">
            <td class="dc" day="7" id="d2012050705" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        7
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="8" id="d2012050805" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        8
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="9" id="d2012050905" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        9
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="10" id="d2012051005" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        10
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="11" id="d2012051105" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        11
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="12" id="d2012051205" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        12
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="13" id="d2012051305" month="5" week="19" year="2012">
                <div class="content">
                    <div class="daynum">
                        13
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
        </tr>
        <tr class="w201220">
            <td class="dc" day="14" id="d2012051405" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        14
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="15" id="d2012051505" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        15
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="16" id="d2012051605" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        16
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="17" id="d2012051705" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        17
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="18" id="d2012051805" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        18
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="19" id="d2012051905" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        19
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="20" id="d2012052005" month="5" week="20" year="2012">
                <div class="content">
                    <div class="daynum">
                        20
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
        </tr>
        <tr class="w201221">
            <td class="dc" day="21" id="d2012052105" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        21
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="22" id="d2012052205" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        22
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="23" id="d2012052305" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        23
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="24" id="d2012052405" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        24
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="25" id="d2012052505" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        25
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="26" id="d2012052605" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        26
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc weekend" day="27" id="d2012052705" month="5" week="21" year="2012">
                <div class="content">
                    <div class="daynum">
                        27
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
        </tr>
        <tr class="w201222">
            <td class="dc" day="28" id="d2012052805" month="5" week="22" year="2012">
                <div class="content">
                    <div class="daynum">
                        28
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="29" id="d2012052905" month="5" week="22" year="2012">
                <div class="content">
                    <div class="daynum">
                        29
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="30" id="d2012053005" month="5" week="22" year="2012">
                <div class="content">
                    <div class="daynum">
                        30
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="dc" day="31" id="d2012053105" month="5" week="22" year="2012">
                <div class="content">
                    <div class="daynum">
                        31
                    </div>
                    <div class="mark">
                    </div>
                </div>
            </td>
            <td class="class" day="1" id="d2012060105" month="6" week="22" year="2012">
                <div class="content">
                    &nbsp;
                </div>
            </td>
            <td class="class" day="2" id="d2012060205" month="6" week="22" year="2012">
                <div class="content">
                    &nbsp;
                </div>
            </td>
            <td class="class" day="3" id="d2012060305" month="6" week="22" year="2012">
                <div class="content">
                    &nbsp;
                </div>
            </td>
        </tr>
    </tbody>
</table>
'''


def test_month_widget():
    "Test the month_widget tag."
    month = ttcal.Month.from_date(datetime.date(2012, 5, 4))
    my_template = template.Template(u'''
    {% load coretags %}
    {% month_widget month full_weeks=False weeknum=False navigation=True daynames="long" %}
    ''')
    rendered = my_template.render(template.Context({"month": month}))
    print rendered.encode('u8')
    assert utidy.utidy(rendered) == utidy.utidy(expected)
