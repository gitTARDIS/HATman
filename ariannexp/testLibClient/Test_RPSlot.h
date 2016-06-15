/* $Id: Test_RPSlot.h,v 1.4 2004/05/03 21:53:40 arianne_rpg Exp $ */
/***************************************************************************
    copyright            : (C) 2004 by Miguel Angel Blanch Lardin
 ***************************************************************************
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
#ifndef __TEST_RPSlot_H__
#define __TEST_RPSlot_H__

#include <cppunit/extensions/HelperMacros.h>
#include <iostream>

#include "../libClient/RPSlot.h"

class Test_RPSlot : public CPPUNIT_NS::TestFixture 
  {
  CPPUNIT_TEST_SUITE( Test_RPSlot );
  CPPUNIT_TEST( testNormal );
  CPPUNIT_TEST( testExceptions );
  CPPUNIT_TEST( testSerialization );
  CPPUNIT_TEST_SUITE_END();
  
  public:
  Test_RPSlot();

  void testNormal();
  void testExceptions();
  void testSerialization();
  };
  
#endif
