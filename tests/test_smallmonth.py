# -*- coding: utf-8 -*-


import datetime
import ttcal

from django import template
from dk import utidy

expected = u'''
<table class="month small-month">
  <thead>

    <tr>
      <th class="month-name" colspan=7 id="m20125">

        Mai, 2012
      </th>
    </tr>

    <tr class="day-name">

      <th>M</th>
      <th>Ti</th>
      <th>O</th>
      <th>To</th>
      <th>F</th>
      <th>L</th>
      <th>S</th>
    </tr>
  </thead>
  <tbody>

    <tr class="w201218">
          <td id="d2012043005" year="2012" month="4" day="30" week="18"
              class="">
                   &nbsp;
          </td>
          <td id="d2012050105" year="2012" month="5" day="1" week="18"
              class="dc">
                1
          </td>
          <td id="d2012050205" year="2012" month="5" day="2" week="18"
              class="dc">
                2
          </td>
          <td id="d2012050305" year="2012" month="5" day="3" week="18"
              class="dc">
                3
          </td>
          <td id="d2012050405" year="2012" month="5" day="4" week="18"
              class="dc">
                4
          </td>
          <td id="d2012050505" year="2012" month="5" day="5" week="18"
              class="dc weekend">
                5
          </td>
          <td id="d2012050605" year="2012" month="5" day="6" week="18"
              class="dc weekend">
                6
          </td>
    </tr>

    <tr class="w201219">
          <td id="d2012050705" year="2012" month="5" day="7" week="19"
              class="dc">
                7
          </td>
          <td id="d2012050805" year="2012" month="5" day="8" week="19"
              class="dc">
                8
          </td>
          <td id="d2012050905" year="2012" month="5" day="9" week="19"
              class="dc">
                9
          </td>
          <td id="d2012051005" year="2012" month="5" day="10" week="19"
              class="dc">
                10
          </td>
          <td id="d2012051105" year="2012" month="5" day="11" week="19"
              class="dc">
                11
          </td>
          <td id="d2012051205" year="2012" month="5" day="12" week="19"
              class="dc weekend">
                12
          </td>
          <td id="d2012051305" year="2012" month="5" day="13" week="19"
              class="dc weekend">
                13
          </td>
    </tr>

    <tr class="w201220">
          <td id="d2012051405" year="2012" month="5" day="14" week="20"
              class="dc">
                14
          </td>
          <td id="d2012051505" year="2012" month="5" day="15" week="20"
              class="dc">
                15
          </td>
          <td id="d2012051605" year="2012" month="5" day="16" week="20"
              class="dc">
                16
          </td>
          <td id="d2012051705" year="2012" month="5" day="17" week="20"
              class="dc">
                17
          </td>
          <td id="d2012051805" year="2012" month="5" day="18" week="20"
              class="dc">
                18
          </td>
          <td id="d2012051905" year="2012" month="5" day="19" week="20"
              class="dc weekend">
                19
          </td>
          <td id="d2012052005" year="2012" month="5" day="20" week="20"
              class="dc weekend">
                20
          </td>
    </tr>

    <tr class="w201221">
          <td id="d2012052105" year="2012" month="5" day="21" week="21"
              class="dc">
                21
          </td>
          <td id="d2012052205" year="2012" month="5" day="22" week="21"
              class="dc">
                22
          </td>
          <td id="d2012052305" year="2012" month="5" day="23" week="21"
              class="dc">
                23
          </td>
          <td id="d2012052405" year="2012" month="5" day="24" week="21"
              class="dc">
                24
          </td>
          <td id="d2012052505" year="2012" month="5" day="25" week="21"
              class="dc">
                25
          </td>
          <td id="d2012052605" year="2012" month="5" day="26" week="21"
              class="dc weekend">
                26
          </td>
          <td id="d2012052705" year="2012" month="5" day="27" week="21"
              class="dc weekend">
                27
          </td>
    </tr>

    <tr class="w201222">
          <td id="d2012052805" year="2012" month="5" day="28" week="22"
              class="dc">
                28
          </td>
          <td id="d2012052905" year="2012" month="5" day="29" week="22"
              class="dc">
                29
          </td>
          <td id="d2012053005" year="2012" month="5" day="30" week="22"
              class="dc">
                30
          </td>
          <td id="d2012053105" year="2012" month="5" day="31" week="22"
              class="dc">
                31
          </td>
          <td id="d2012060105" year="2012" month="6" day="1" week="22"
              class="">
                   &nbsp;
          </td>
          <td id="d2012060205" year="2012" month="6" day="2" week="22"
              class="">
                   &nbsp;
          </td>
          <td id="d2012060305" year="2012" month="6" day="3" week="22"
              class="">
                   &nbsp;
          </td>
    </tr>

  </tbody>
</table>
'''


def test_small_month_widget():
    "Test the small_month_widget tag."
    month = ttcal.Month.from_date(datetime.date(2012, 5, 4))
    my_template = template.Template('''
        {% load coretags %}
        {% small_month_widget month full_weeks=False weeknum=False%}
        ''')
    rendered = utidy.utidy(my_template.render(template.Context({"month": month})))
    print rendered
    assert rendered == utidy.utidy(expected)
